from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from app.core.text_cleaner import normalize, remove_stopwords
from app.core.data_loader import load_df

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    party: str | None = None
    member: str | None = None

@router.post("/")
async def search(request: SearchRequest):
    """
    Ολοκληρωμένη αναζήτηση κατά πλήρες κείμενο (full-text search) στα ομιλητήρια του Ελληνικού Κοινοβουλίου.
    
    1. Κανονικοποιεί και αφαιρεί stopwords από το query
    2. Διαιρεί το query σε μεμονωμένους όρους
    3. Υπολογίζει score ανά ομιλία βάσει συχνότητας εμφάνισης των όρων
    4. Εφαρμόζει φίλτρα κόμματος/μέλους αν επιλεγούν
    5. Ταξινομεί αποτελέσματα κατά score σε φθίνουσα σειρά
    6. Επιστρέφει τα κορυφαία top_k αποτελέσματα με snippet (απόσπασμα 300 χαρακτήρων)
    
    """
    query_norm = remove_stopwords(normalize(request.query))
    if not query_norm:
        return {"query": request.query, "results": []}

    terms = query_norm.split()

    df = load_df()
    df = df.dropna(subset=["speech", "member_name", "political_party", "sitting_date"])

    speech_norm = df["speech"].astype(str).apply(normalize)
    member_norm = df["member_name"].astype(str).apply(normalize)
    party_norm = df["political_party"].astype(str).apply(normalize)

    scores = pd.Series(0, index=df.index)
    for term in terms:
        scores += speech_norm.str.count(rf"\b{term}\b")

    df["score"] = scores
    df = df[df["score"] > 0]

    if request.party:
        party_q = normalize(request.party)
        df = df[party_norm.str.contains(party_q, na=False)]
    if request.member:
        member_q = normalize(request.member)
        df = df[member_norm.str.contains(member_q, na=False)]

    df = df.sort_values("score", ascending=False)

    results_df = df.head(request.top_k)[
        ["sitting_date", "member_name", "political_party", "speech", "score"]
    ]
    results_df["snippet"] = results_df["speech"].astype(str).str.slice(0, 300)

    return {
        "query": request.query,
        "results": results_df[["sitting_date", "member_name", "political_party", "snippet", "score"]].to_dict(orient="records")
    }
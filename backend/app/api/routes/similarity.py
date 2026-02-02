from fastapi import APIRouter, Query
from collections import Counter
from app.core.text_cleaner import normalize, remove_stopwords
from app.core.data_loader import load_df

router = APIRouter()

def extract_keywords(text: str, top_n: int = 20):
    text = remove_stopwords(normalize(text))
    words = [w for w in text.split() if len(w) > 2]
    return [w for w, _ in Counter(words).most_common(top_n)]

def jaccard(a: set, b: set) -> float:
    """
    Υπολογισμός Jaccard Similarity ανάμεσα σε δύο σύνολα λέξεων.
    
    Τύπος: |A ∩ B| / |A ∪ B|

    """
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)

@router.get("/top-pairs")
async def top_pairs(
    limit_members: int = Query(50, ge=5, le=300),
    top_terms: int = Query(20, ge=5, le=50),
    top_k: int = Query(5, ge=1, le=100)
):
    """
    Εύρεση των πιο ομοίων ζευγών μελών του κοινοβουλίου βάσει των θεμάτων τους.
    
    1. Επιλέγει τα πρώτα limit_members μέλη από το dataset
    2. Ομαδοποιεί ομιλίες ανά μέλος και συνδυάζει το κείμενό τους
    3. Εξάγει τις κορυφαίες top_terms λέξεις-κλειδιά για κάθε μέλος
    4. Υπολογίζει Jaccard Similarity ανάμεσα σε όλα τα ζεύγη μελών
    5. Επιστρέφει τα top_k ζεύγη με τη μεγαλύτερη ομοιότητα
    
    """
    df = load_df()
    df = df.dropna(subset=["speech", "member_name"])

    members = df["member_name"].unique()[:limit_members]
    df = df[df["member_name"].isin(members)]

    grouped = df.groupby("member_name")["speech"].apply(lambda x: " ".join(x)).reset_index()

    member_keywords = {}
    for _, row in grouped.iterrows():
        member = row["member_name"]
        kw = set(extract_keywords(row["speech"], top_terms))
        member_keywords[member] = kw

    pairs = []
    members_list = list(member_keywords.keys())
    for i in range(len(members_list)):
        for j in range(i + 1, len(members_list)):
            m1 = members_list[i]
            m2 = members_list[j]
            sim = jaccard(member_keywords[m1], member_keywords[m2])
            pairs.append({"member_1": m1, "member_2": m2, "similarity": sim})

    pairs = sorted(pairs, key=lambda x: x["similarity"], reverse=True)[:top_k]
    return {"limit_members": limit_members, "top_k": top_k, "pairs": pairs}
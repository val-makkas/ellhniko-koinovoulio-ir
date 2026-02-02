from fastapi import APIRouter, Query
import pandas as pd
from collections import Counter
from app.core.text_cleaner import normalize, remove_stopwords
from app.core.data_loader import load_df

router = APIRouter()

def extract_keywords(text: str, top_n: int = 10):
    """
    Εξαγωγή κορυφαίων λέξεων-κλειδιών από κείμενο.
    
    1. Κανονικοποιεί και αφαιρεί stopwords (άχρηστες λέξεις)
    2. Φιλτράρει λέξεις με λιγότερα από 3 γράμματα (θόρυβος)
    3. Μετράει συχνότητα κάθε λέξης
    4. Επιστρέφει τις top_n πιο συχνές λέξεις

    """
    text = remove_stopwords(normalize(text))
    words = [w for w in text.split() if len(w) > 2]
    return [w for w, _ in Counter(words).most_common(top_n)]

@router.get("/member-timeline")
async def keywords_member_timeline(
    name: str = Query(..., min_length=2),
    top_n: int = Query(10, ge=1, le=50)
):
    """
    Εξαγωγή χρονολογικής εξέλιξης κύριων θεμάτων ανά μέλος του κοινοβουλίου.
    
    1. Φιλτράρει ομιλίες ενός συγκεκριμένου μέλους
    2. Εξαγωγή του έτους από την ημερομηνία κάθε ομιλίας
    3. Ομαδοποιεί ομιλίες ανά έτος
    4. Για κάθε έτος: συνδυάζει όλες τις ομιλίες και εξάγει κορυφαίες λέξεις-κλειδιά
    5. Επιστρέφει τη χρονολογική σειρά θεμάτων
    
    """
    df = load_df()
    df = df.dropna(subset=["speech", "member_name", "sitting_date"])

    mask = df["member_name"].astype(str).str.contains(name, case=False, na=False)
    df = df[mask].copy()

    df["year"] = pd.to_datetime(df["sitting_date"], dayfirst=True, errors="coerce").dt.year
    df = df.dropna(subset=["year"])

    timeline = []
    for year, group in df.groupby("year"):
        text = " ".join(group["speech"].astype(str).tolist())
        timeline.append({"year": int(year), "keywords": extract_keywords(text, top_n)})

    timeline = sorted(timeline, key=lambda x: x["year"])
    return {"member": name, "timeline": timeline}

@router.get("/party-timeline")
async def keywords_party_timeline(
    party: str = Query(..., min_length=2),
    top_n: int = Query(10, ge=1, le=50)
):
    """
    Εξαγωγή χρονολογικής εξέλιξης κύριων θεμάτων ανά κόμμα.
    
    1. Φιλτράρει ομιλίες ενός συγκεκριμένου κόμματος
    2. Εξαγωγή του έτους από την ημερομηνία κάθε ομιλίας
    3. Ομαδοποιεί ομιλίες ανά έτος
    4. Για κάθε έτος: συνδυάζει όλες τις ομιλίες και εξάγει κορυφαίες λέξεις-κλειδιά
    5. Επιστρέφει τη χρονολογική εξέλιξη θεμάτων του κόμματος
    
    """
    df = load_df()
    df = df.dropna(subset=["speech", "political_party", "sitting_date"])

    mask = df["political_party"].astype(str).str.contains(party, case=False, na=False)
    df = df[mask].copy()

    df["year"] = pd.to_datetime(df["sitting_date"], dayfirst=True, errors="coerce").dt.year
    df = df.dropna(subset=["year"])

    timeline = []
    for year, group in df.groupby("year"):
        text = " ".join(group["speech"].astype(str).tolist())
        timeline.append({"year": int(year), "keywords": extract_keywords(text, top_n)})

    timeline = sorted(timeline, key=lambda x: x["year"])
    return {"party": party, "timeline": timeline}

@router.get("/speech")
async def keywords_from_speech(
    speech_index: int = Query(..., ge=0),
    top_n: int = Query(10, ge=1, le=50)
):
    """
    Εξαγωγή κορυφαίων λέξεων-κλειδιών από μία μεμονωμένη ομιλία.
    
    1. Φορτώνει όλες τις ομιλίες από το dataset
    2. Επιλέγει την ομιλία με το δοσμένο index
    3. Εξάγει τις κορυφαίες λέξεις-κλειδιά
    4. Επιστρέφει τα στοιχεία της ομιλίας (μέλος, κόμμα, ημερομηνία) με τις λέξεις-κλειδιά

    """
    df = load_df()
    df = df.dropna(subset=["speech", "member_name", "political_party", "sitting_date"])
    
    if speech_index >= len(df) or speech_index < 0:
        return {"error": "Speech index out of range"}
    
    row = df.iloc[speech_index]
    speech_text = row["speech"]
    keywords = extract_keywords(speech_text, top_n)
    
    return {
        "speech_index": speech_index,
        "member_name": row["member_name"],
        "political_party": row["political_party"],
        "sitting_date": row["sitting_date"],
        "keywords": keywords
    }
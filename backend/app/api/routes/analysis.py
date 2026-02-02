from fastapi import APIRouter, Query
import pandas as pd
from collections import Counter
from app.core.text_cleaner import normalize, remove_stopwords
from app.core.data_loader import load_df

router = APIRouter()

def extract_keywords(text: str, top_n: int = 10):
    """
    Εξαγωγή κορυφαίων λέξεων-κλειδιών από κείμενο.
    
    1. Κανονικοποιεί και αφαιρεί stopwords
    2. Φιλτράρει λέξεις με λιγότερα από 3 γράμματα
    3. Μετράει συχνότητα κάθε λέξης
    4. Επιστρέφει τις top_n πιο συχνές λέξεις
    
    """
    text = remove_stopwords(normalize(text))
    words = [w for w in text.split() if len(w) > 2]
    return [w for w, _ in Counter(words).most_common(top_n)]

@router.get("/topic-drift")
async def topic_drift(
    start_year: int = Query(1989, ge=1989, le=2020),
    end_year: int = Query(2020, ge=1989, le=2020),
    top_n: int = Query(8, ge=1, le=20)
):
    """
    Ανάλυση εξέλιξης θεμάτων κατά τη διάρκεια των χρόνων (Topic Drift).
    
    1. Φορτώνει ομιλίες του κοινοβουλίου
    2. Εξαγωγή έτους από ημερομηνία κάθε ομιλίας
    3. Φιλτράρει ομιλίες για το χρονικό διάστημα [start_year, end_year]
    4. Ομαδοποιεί ομιλίες ανά έτος
    5. Για κάθε έτος: συνδυάζει όλες τις ομιλίες και εξάγει κορυφαίες λέξεις-κλειδιά
    6. Δημιουργεί χρονολογικό πίνακα θεμάτων δείχνοντας πώς εξελίχθησαν τα θέματα

    """
    if start_year > end_year:
        return {"error": "start_year must be <= end_year"}
    
    df = load_df()
    df = df.dropna(subset=["speech", "sitting_date"]).copy()
    
    df["year"] = pd.to_datetime(df["sitting_date"], dayfirst=True, errors="coerce").dt.year
    df = df[df["year"].between(start_year, end_year)]
    
    timeline = []
    for year in sorted(df["year"].unique()):
        year_data = df[df["year"] == year]
        text = " ".join(year_data["speech"].astype(str).tolist())
        keywords = extract_keywords(text, top_n)
        timeline.append({"year": int(year), "topics": keywords})
    
    return {
        "analysis": "topic_drift",
        "period": f"{start_year}-{end_year}",
        "timeline": timeline
    }

@router.get("/topic-drift-by-party")
async def topic_drift_by_party(
    party: str = Query(..., min_length=2),
    start_year: int = Query(1989, ge=1989, le=2020),
    end_year: int = Query(2020, ge=1989, le=2020),
    top_n: int = Query(8, ge=1, le=20)
):
    """
    Ανάλυση εξέλιξης θεμάτων ενός συγκεκριμένου κόμματος κατά τη διάρκεια των χρόνων.
    
    1. Φορτώνει ομιλίες του κοινοβουλίου
    2. Φιλτράρει ομιλίες του συγκεκριμένου κόμματος
    3. Εξαγωγή έτους από ημερομηνία κάθε ομιλίας
    4. Φιλτράρει για το χρονικό διάστημα [start_year, end_year]
    5. Ομαδοποιεί ομιλίες ανά έτος
    6. Για κάθε έτος: εξάγει κορυφαίες λέξεις-κλειδιά του κόμματος
    7. Δείχνει πώς μεταβλήθησε η εστίαση του κόμματος χρονικά

    """
    if start_year > end_year:
        return {"error": "start_year must be <= end_year"}
    
    df = load_df()
    df = df.dropna(subset=["speech", "political_party", "sitting_date"]).copy()
    
    mask = df["political_party"].astype(str).str.contains(party, case=False, na=False)
    df = df[mask].copy()
    
    df["year"] = pd.to_datetime(df["sitting_date"], dayfirst=True, errors="coerce").dt.year
    df = df[df["year"].between(start_year, end_year)]
    
    timeline = []
    for year in sorted(df["year"].unique()):
        year_data = df[df["year"] == year]
        text = " ".join(year_data["speech"].astype(str).tolist())
        keywords = extract_keywords(text, top_n)
        timeline.append({"year": int(year), "topics": keywords})
    
    return {
        "analysis": "party_topic_drift",
        "party": party,
        "period": f"{start_year}-{end_year}",
        "timeline": timeline
    }

@router.get("/topic-comparison")
async def topic_comparison(
    year1: int = Query(2008, ge=1989, le=2020),
    year2: int = Query(2020, ge=1989, le=2020),
    top_n: int = Query(10, ge=1, le=20)
):
    """
    Σύγκριση θεμάτων ανάμεσα σε δύο διαφορετικά έτη.
    
    Διαδικασία:
    1. Φορτώνει ομιλίες του κοινοβουλίου
    2. Για κάθε ένα από τα δύο έτη:
       - Φιλτράρει ομιλίες του έτους
       - Συνδυάζει όλες τις ομιλίες
       - Εξάγει κορυφαίες λέξεις-κλειδιά
       - Καταγράφει το αριθμό ομιλιών του έτους
    3. Δείχνει πώς διαφέρουν τα θέματα ανάμεσα στα δύο έτη

    """
    df = load_df()
    df = df.dropna(subset=["speech", "sitting_date"]).copy()
    
    df["year"] = pd.to_datetime(df["sitting_date"], dayfirst=True, errors="coerce").dt.year
    
    results = {}
    for year in [year1, year2]:
        year_data = df[df["year"] == year]
        if len(year_data) > 0:
            text = " ".join(year_data["speech"].astype(str).tolist())
            results[year] = {
                "topics": extract_keywords(text, top_n),
                "speech_count": len(year_data)
            }
        else:
            results[year] = {"error": "No data for this year"}
    
    return {
        "analysis": "year_comparison",
        "comparison": results
    }
from fastapi import APIRouter, Query
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from app.core.text_cleaner import normalize, remove_stopwords
from app.core.data_loader import load_df

router = APIRouter()

def preprocess(text: str) -> str:
    """
    Προ-επεξεργασία κειμένου για αναζήτηση LSI.
    
    1. Κανονικοποιεί το κείμενο (πεζά γράμματα, αφαίρεση διακριτικών)
    2. Αφαιρεί stopwords

    """
    return remove_stopwords(normalize(text))

@router.get("/topics")
async def lsi_topics(
    sample_size: int = Query(500, ge=100, le=2000),
    n_topics: int = Query(5, ge=2, le=20),
    top_terms: int = Query(10, ge=5, le=30)
):
    """
    Εξαγωγή λανθάνουσων σημασιολογικών θεμάτων χρησιμοποιώντας Latent Semantic Indexing (LSI).
    
    1. Φόρτωση δεδομένων και δημιουργία δείγματος ομιλιών
    2. Προ-επεξεργασία κειμένων (κανονικοποίηση, αφαίρεση stopwords)
    3. TF-IDF Vectorization: Μετατροπή κειμένων σε αριθμητικά διανύσματα
    4. Truncated SVD: Μείωση διαστάσεων για εξαγωγή λανθάνουσων σημασιολογικών διαστάσεων
    5. Εξαγωγή κορυφαίων όρων για κάθε θέμα (topic)
    
    """
    df = load_df()
    df = df.dropna(subset=["speech"])
    df = df.head(sample_size)

    docs = df["speech"].astype(str).apply(preprocess).tolist()

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(docs)

    svd = TruncatedSVD(n_components=n_topics, random_state=42)
    svd.fit(X)

    terms = vectorizer.get_feature_names_out()
    topics = []
    for i, comp in enumerate(svd.components_):
        top_idx = comp.argsort()[-top_terms:][::-1]
        topics.append({
            "topic_id": i,
            "terms": [terms[j] for j in top_idx]
        })

    return {
        "sample_size": sample_size,
        "n_topics": n_topics,
        "topics": topics
    }
from fastapi import APIRouter, Query
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from app.core.text_cleaner import normalize, remove_stopwords
from app.core.data_loader import load_df

router = APIRouter()

def preprocess(text: str) -> str:
    """
    Προ-επεξεργασία κειμένου για ομαδοποίηση (clustering).
    
    1. Κανονικοποιεί το κείμενο (πεζά γράμματα, αφαίρεση διακριτικών)
    2. Αφαιρεί stopwords
    
    """
    return remove_stopwords(normalize(text))

@router.get("/groups")
async def cluster_speeches(
    sample_size: int = Query(500, ge=100, le=2000),
    n_clusters: int = Query(5, ge=2, le=20),
    top_terms: int = Query(8, ge=3, le=20)
):
    """
    Ομαδοποίηση ομιλιών χρησιμοποιώντας K-Means clustering αλγόριθμο.
    
    1. Φόρτωση δεδομένων και δημιουργία δείγματος ομιλιών
    2. Προ-επεξεργασία κειμένων (κανονικοποίηση, αφαίρεση stopwords)
    3. TF-IDF Vectorization: Μετατροπή κειμένων σε αριθμητικά διανύσματα
    4. K-Means: Ομαδοποίηση σε n_clusters ομάδες με βάσει τη συνάφεια περιεχομένου
    5. Εξαγωγή κορυφαίων όρων για κάθε ομάδα

    """
    df = load_df()
    df = df.dropna(subset=["speech"])
    df = df.head(sample_size)

    docs = df["speech"].astype(str).apply(preprocess).tolist()

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(docs)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(X)

    terms = vectorizer.get_feature_names_out()
    cluster_terms = []
    for i in range(n_clusters):
        center = kmeans.cluster_centers_[i]
        top_idx = center.argsort()[-top_terms:][::-1]
        cluster_terms.append({
            "cluster_id": i,
            "terms": [terms[j] for j in top_idx],
            "size": int((labels == i).sum())
        })

    return {
        "sample_size": sample_size,
        "n_clusters": n_clusters,
        "clusters": cluster_terms
    }
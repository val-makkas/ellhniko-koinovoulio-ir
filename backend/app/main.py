"""
FastAPI application server για το Greek Parliament Information Retrieval System.

Αυτή είναι η κύρια εφαρμογή που παρέχει RESTful API endpoints για:
- Αναζήτηση ομιλιών (full-text search)
- Εξαγωγή λέξεων-κλειδιών και ανάλυση χρονολογικής εξέλιξης
- Υπολογισμό ομοιότητας μελών κοινοβουλίου
- LSI (Latent Semantic Indexing) για ανακάλυψη θεμάτων
- K-Means clustering για ομαδοποίηση ομιλιών
- Ανάλυση εξέλιξης θεμάτων (topic drift)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.search import router as search_router
from app.api.routes.data import router as data_router
from app.api.routes.speeches import router as speeches_router
from app.api.routes.keywords import router as keywords_router
from app.api.routes.similarity import router as similarity_router
from app.api.routes.lsi import router as lsi_router
from app.api.routes.clustering import router as clustering_router
from app.api.routes.analysis import router as analysis_router

app = FastAPI(title="Greek Parliament IR API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router, prefix="/api/search", tags=["Search"])
app.include_router(data_router, prefix="/api/data", tags=["Data"])
app.include_router(speeches_router, prefix="/api/speeches", tags=["Speeches"])
app.include_router(keywords_router, prefix="/api/keywords", tags=["Keywords"])
app.include_router(similarity_router, prefix="/api/similarity", tags=["Similarity"])
app.include_router(lsi_router, prefix="/api/lsi", tags=["LSI"])
app.include_router(clustering_router, prefix="/api/clustering", tags=["Clustering"])
app.include_router(analysis_router, prefix="/api/analysis", tags=["Analysis"])

@app.get("/")
async def root():
    return {"message": "API is running"}
# Greek Parliament Information Retrieval & Analysis

## Περιγραφή
Το project παρέχει μια πλήρη πλατφόρμα αναζήτησης και ανάλυσης ομιλιών του Ελληνικού Κοινοβουλίου. Περιλαμβάνει backend API (FastAPI) για επεξεργασία φυσικής γλώσσας και ανάλυση δεδομένων, και frontend (React + Vite) για τη διάδραση με τον χρήστη.

## Dataset
Το σύστημα βασίζεται στο αρχείο:
- `backend/data/Greek_Parliament_Proceedings_1989_2020.csv`

Απαραίτητες στήλες:
- `speech` (κείμενο ομιλίας)
- `member_name` (ομιλητής)
- `political_party` (κόμμα)
- `sitting_date` (ημερομηνία συνεδρίασης)

## Τεχνική Ανάλυση
### 1) Προ-επεξεργασία κειμένου
- Κανονικοποίηση ελληνικού κειμένου (πεζά, αφαίρεση τόνων/διακριτικών, ειδικών χαρακτήρων)
- Αφαίρεση stopwords (ελληνική λίστα)
- Καθαρισμός κενών και μη χρήσιμων συμβόλων

### 2) Αναζήτηση πλήρους κειμένου
- Κανονικοποίηση ερωτήματος
- Διάσπαση σε όρους
- Υπολογισμός score βάσει συχνότητας εμφάνισης των όρων στην ομιλία
- Φίλτρα ανά κόμμα και μέλος
- Επιστροφή top-$k$ αποτελεσμάτων με snippet

### 3) Εξαγωγή λέξεων-κλειδιών
- Μετρήσεις συχνοτήτων (Counter)
- Επιστροφή κορυφαίων λέξεων-κλειδιών ανά ομιλία, ανά μέλος ή ανά κόμμα
- Χρονολογική ανάλυση (timeline) ανά έτος

### 4) Ομοιότητα μελών
- Συλλογή κορυφαίων όρων ανά μέλος
- Υπολογισμός Jaccard similarity σε σύνολα λέξεων
- Επιστροφή κορυφαίων ζευγών ομοιότητας

### 5) LSI (Latent Semantic Indexing)
- TF-IDF vectorization
- Truncated SVD για μείωση διαστάσεων
- Εξαγωγή κορυφαίων όρων ανά θέμα

### 6) Ομαδοποίηση ομιλιών (Clustering)
- TF-IDF vectorization
- K-Means clustering
- Περιγραφή ομάδων με κορυφαίους όρους

### 7) Ανάλυση εξέλιξης θεμάτων
- Topic drift συνολικά ή ανά κόμμα
- Σύγκριση θεμάτων μεταξύ ετών

## Αρχιτεκτονική
- **Backend (FastAPI)**: REST API endpoints για αναζήτηση, ανάλυση, LSI και clustering.
- **Frontend (React + Vite)**: UI για αναζήτηση και ανάλυση (tabs Search, Timeline, Topic Drift).
- **Data Layer**: CSV dataset, φόρτωση μέσω Pandas με cache.

### Endpoints (ενδεικτικά)
- `POST /api/search/`
- `GET /api/keywords/member-timeline`
- `GET /api/keywords/party-timeline`
- `GET /api/similarity/top-pairs`
- `GET /api/lsi/topics`
- `GET /api/clustering/groups`
- `GET /api/analysis/topic-drift`

## Εκτέλεση με Docker
### Windows
1. Βεβαιώσου ότι είναι εγκατεστημένο το Docker Desktop.
2. Εκτέλεσε το script:
   - `setup-docker.bat`

### macOS/Linux
1. Βεβαιώσου ότι είναι εγκατεστημένο το Docker.
2. Δώσε δικαιώματα εκτέλεσης:
   - `chmod +x setup-docker.sh`
3. Εκτέλεσε το script:
   - `./setup-docker.sh`

### Τι θα ανοίξει
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## Scripts
- **setup-docker.bat**: Έλεγχος Docker/Compose, προειδοποίηση αν λείπει το CSV, build & run containers.
- **setup-docker.sh**: Αντίστοιχο script για macOS/Linux.

## Εκτέλεση χωρίς Docker
### Backend
1. Δημιουργία virtual environment:
   - `python -m venv venv`
2. Ενεργοποίηση:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Εγκατάσταση dependencies:
   - `pip install -r backend/requirements.txt`
4. Εκκίνηση API:
   - `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Δομή Φακέλων (σύνοψη)
```
backend/
  app/
    api/routes/
    core/
  data/
frontend/
  src/
docker-compose.yml
setup-docker.bat
setup-docker.sh
```
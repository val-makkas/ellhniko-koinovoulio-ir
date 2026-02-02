import re
from app.core.stopwords import STOPWORDS

ACCENTS_TABLE = str.maketrans(
    "άέήίόύώϊΐϋΰὰὲὴὶὸὺὼᾶῆῖῦῶ",
    "αεηιουωιιυυαεηιουωαηιυω"
)

UNWANTED = re.compile(r"[0-9@#$%^&*()\-_=+\[\]{};:'\",.<>/?\\|`~!]")

def normalize(text: str) -> str:
    """
    Κανονικοποίηση ελληνικού κειμένου.
    
    1. Ελέγχει αν το κείμενο είναι κενό
    2. Μετατρέπει σε πεζά γράμματα
    3. Αφαιρεί διακριτικά σημάτα (άκουτα, περισπώμενα)
    4. Αφαιρεί αριθμούς, σύμβολα, και ειδικούς χαρακτήρες
    5. Αφαιρεί περισσότερα από ένα κενά (normalize whitespace)
    6. Αφαιρεί κενά στην αρχή και το τέλος

    """
    if not text:
        return ""
    text = text.lower().translate(ACCENTS_TABLE)
    text = re.sub(UNWANTED, " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

STOPWORDS_NORM = {normalize(w) for w in STOPWORDS}

def remove_stopwords(text: str) -> str:
    """
    Αφαίρεση stopwords (άχρηστων λέξεων) από κείμενο.
    
    1. Διαιρεί το κείμενο σε λέξεις (tokens)
    2. Φιλτράρει λέξεις που βρίσκονται στη λίστα stopwords
    3. Συνδυάζει τις εναπομείνασες λέξεις
    
    """
    words = [w for w in text.split() if w not in STOPWORDS_NORM]
    return " ".join(words)
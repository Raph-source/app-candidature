"""
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import joblib  # pour sauvegarder le modèle

# Données d'entraînement (idéalement, plus de lignes)
data = {
    "diplome_info": [1, 1, 0, 1, 1, 0],
    "experience":   [1, 0, 1, 1, 0, 0],
    "anglais":      [1, 1, 1, 0, 1, 0],
    "langage_prog": [1, 1, 1, 1, 0, 0],
    "valide":       [1, 0, 0, 0, 0, 0]
}

df = pd.DataFrame(data)

X = df[["diplome_info", "experience", "anglais", "langage_prog"]]
y = df["valide"]

# Entraînement
model = DecisionTreeClassifier()
model.fit(X, y)

# Sauvegarde
joblib.dump(model, "../../storage/modele_informatique.pkl")

"""
import joblib
import re
from PyPDF2 import PdfReader
import unicodedata
from pdf2image import convert_from_path
import pytesseract
import os


# Charger le modèle entraîné
model = joblib.load("../../storage/modele_informatique.pkl")

# Fonction pour extraire le texte d’un fichier PDF
def extraire_texte_pdf(chemin_pdf: str) -> str:
    lecteur = PdfReader(chemin_pdf)
    texte = ""
    for page in lecteur.pages:
        texte += page.extract_text()
    return texte.lower()

def nettoyer_texte(texte: str) -> str:
    # Supprimer les sauts de ligne et les espaces anormaux
    texte = texte.replace('\n', ' ').replace('\r', ' ')
    texte = re.sub(r'\s+', ' ', texte)  # Espaces multiples → un seul

    # Corriger les mots cassés (ex. : "expérienc e" → "expérience")
    texte = re.sub(r'exp[ée]rienc\s+e', 'expérience', texte, flags=re.IGNORECASE)
    
    # Normaliser les accents (é → é)
    texte = unicodedata.normalize("NFKC", texte)

    return texte.lower()

def ocr_depuis_pdf(pdf_path):
    # Convertit les pages du PDF en images
    images = convert_from_path(pdf_path)
    texte_complet = ""

    for image in images:
        # Applique l'OCR sur chaque image
        texte = pytesseract.image_to_string(image, lang='fra')
        texte_complet += texte + "\n"

    return texte_complet.lower()

# Fonction pour extraire les features du CV
def extraire_features(texte: str) -> list[int]:
    texte = nettoyer_texte(texte=texte)

    feature_diplome = int(bool(re.search(r"(licence|master|bac\+3|bac\+5).*(informatique|computer)", texte)))
    feature_experience = int(bool(re.search(r"(\d+)\s*(ans|an)\s+.*(informatique|développement|développeur)", texte)))
    feature_anglais = int("anglais" in texte or "english" in texte)
    feature_programmation = int(bool(re.search(r"\b(python|java|c\+\+|c#|javascript|php)\b", texte)))

    print(texte)
    print(feature_diplome)
    print(feature_experience)
    print(feature_anglais)
    print(feature_programmation)
    return [feature_diplome, feature_experience, feature_anglais, feature_programmation]

# Exemple d’utilisation
if __name__ == "__main__":
    chemin_cv = "../../uploads/test.pdf"  # Remplace par le vrai chemin du fichier
    texte_cv = extraire_texte_pdf(chemin_cv)
    features = [extraire_features(texte_cv)]

    prediction = model.predict(features)
    print("Valide" if prediction[0] == 1 else "Non valide")

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

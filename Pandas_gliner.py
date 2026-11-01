#création d'un path et sortie avec os
import os 
import pandas as pd
from gliner2 import AutoExtractor
path = "S:/CEM/CORPUS-CEM-TXM"
## modèle : python -m pip install "gliner2[local]"
model = AutoExtractor.from_pretrained("fastino/gliner2.5-multi-v1")

print(os.getcwd())

# parcourir la liste des tsv 
for doc in os.listdir(path):
    if doc.endswith(".tsv"):
        fichier = os.path.join(path, doc)
        df = pd.read_csv(fichier, sep="\t", dtype=str, keep_default_na=False)
        df.head()
        mot = df["index_u"].unique()
        for numero in mot: 
            mots = df[df["index_u"] == numero]["forme"]
            texte =" ".join(mots)
            resultat = model.extract_entities(texte,["person", "location"])
            print(resultat)
            break
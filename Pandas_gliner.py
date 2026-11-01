#création d'un path et sortie avec os
import os 
import pandas as pd

## modèle : python -m pip install "gliner2[local]"
path = "S:/CEM/CORPUS-CEM-TXM"
print(os.getcwd())

# parcourir la liste des tsv 
for doc in os.listdir(path):
    if doc.endswith(".tsv"):
        fichier = os.path.join(path, doc)
        df = pd.read_csv(fichier, sep="\t", dtype=str, keep_default_na=False)
print(df.head())

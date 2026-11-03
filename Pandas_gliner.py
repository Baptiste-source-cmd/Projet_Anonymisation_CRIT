#création d'un path et sortie avec os
import os 
import pandas as pd
from gliner2 import AutoExtractor
import xml.etree.ElementTree as ET
path = "S:/CEM/CORPUS-CEM-TXM"
## modèle : python -m pip install "gliner2[local]"
model = AutoExtractor.from_pretrained("fastino/gliner2.5-multi-v1")
print(os.getcwd())

sortie = os.path.join(path, "résultats")
os.makedirs(sortie, exist_ok=True)

# parcourir la liste des tsv 
for doc in os.listdir(path):
    if doc.endswith(".tsv"):
        fichier = os.path.join(path, doc)
        print(doc)
        df = pd.read_csv(fichier, sep="\t", dtype=str, keep_default_na=False)
        df.head()

        #préparation colonne vide pour xmliser gliner
        df["annoté"] = df["forme"]
        texte_xmlisé = []
         
        # reconstitution en phrases
        resultats = []
        mot = df["index_u"].unique()  # permet d'extraire les doublons
        for numero in mot: #compte l'ensemble de l'index (à quelle séquence de <u> ils appartiennent), et chaque valeur ne peut apparaître qu'une seule fois : c'est pratique parce que les données sont coupées par mots, ça évite de répéter mon comptage
            comptage_phrase = df[df["index_u"] == numero]
            mots = comptage_phrase["forme"]
            texte =" ".join(mots)
            
          # extraction données par gliner  
            resultat = model.extract_entities(texte,{
            "person": "Prénoms et noms de personnes, y compris les prénoms seuls, rares ou peu fréquents, notamment après des expressions comme je m'appelle, mon prénom est, moi c'est",
            "location": "Noms propres de lieux géographiques et de régions, à l'exclusion des villes, des pays, des noms communs et des expressions spatiales vagues",
            "organization": "Noms propres d'organisations, d'entreprises, d'associations et d'institutions, à l'exclusion des noms génériques d'institutions",
            "city": "Noms propres de villes et de communes",
            "country": "Noms propres de pays et d'États souverains",
            "origine": "Gentilés, noms et adjectifs désignant l'appartenance ou l'origine géographique, nationale ou régionale de personnes ou de groupes humains, au singulier comme au pluriel, au masculin comme au féminin"},include_confidence=True,include_spans=True,)
            print(texte)
            print(resultat)
        
            resultats.append(f"{texte}\n{resultat}\n")
#annotation xml 

            texte_annoté = texte ##je reprends mon texte pour éviter de casser gliner qui utilise la variable texte
            positions = [] ## j'ai besoin de savoir où commence mes éléments à annoter et j'utilise donc include_spans (qui me permet de savoir quand entité démarre dans la phrase) et je l'introduit dans positions

            
            for cat, entités in resultat["entities"].items(): #exemple gliner : {'entities': {'person': [{'text': 'magistère', 'confidence': 0.7929778099060059, 'start': 10, 'end': 19}], 'location': []}}
                    for entité in entités:
                        balise = ET.Element(cat) ## https://docs.python.org/3/library/xml.etree.elementtree.html#building-xml-documents
                        balise.text = entité["text"] ## avec include_spans, entities devient un dictionnaire et plus un tuple, il faut que j'annote uniquement "text"
                        xml = ET.tostring(balise, encoding="unicode") ##permet de transformer les balises elementTree en string manipulables
                        positions.append((entité["start"], entité["end"], xml))# Source - https://stackoverflow.com/a/6304835  
                        
            limite = None
            for start, end, xml in sorted(positions, reverse=True):
                if limite is None or end <= limite:
                    texte_annoté = (f"{texte_annoté[:start]}{xml}{texte_annoté[end:]}) # Source - https://stackoverflow.com/a/59965745 [end] renvoyait une erreur d'indexage, sans :, la séquence s'arrête pas après "end"
                    limite = start 
                print(texte_annoté)
                
            df.loc[mots.index, "annoté"] = texte_annoté.split(" ")
            texte_xmlisé.append(texte_annoté)




        # soretie du document
        gliner_brute = os.path.join(sortie, doc.replace(".tsv", "_NER.txt"))
        nouveau_xmlisé = os.path.join(sortie, doc.replace(".tsv", "_annoté.txt"))
        nouveau_tsv = os.path.join(sortie, doc.replace(".tsv", "modifié.tsv"))
        with open(nouveau_xmlisé, "w", encoding="utf-8") as f:
            f.write("\n".join(texte_xmlisé))
        with open (gliner_brute, "w", encoding="utf-8") as f:
            f.write("\n".join(resultats))
        with open (nouveau_tsv, "w", encoding="utf-8") as f:
            f.write(df.to_csv(sep="\t"))
        break
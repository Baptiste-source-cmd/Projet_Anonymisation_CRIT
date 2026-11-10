#création d'un path et sortie avec os
import os 
import pandas as pd
from gliner2 import AutoExtractor
import xml.etree.ElementTree as ET
path = "S:/CEM/CORPUS-CEM-TXM"
## modèle : python -m pip install "gliner2[local]"
model = AutoExtractor.from_pretrained("fastino/gliner2.5-multi-v1")
print(os.getcwd())



# parcourir la liste des tsv 
for doc in os.listdir(path):
    if doc.endswith(".tsv"):
        fichier = os.path.join(path, doc)
        print(doc)
        df = pd.read_csv(fichier, sep="\t", dtype=str, keep_default_na=False)
        df.head()
        sortie = os.path.join(path, f"résultats/{doc.replace(".tsv","")}")
        os.makedirs(sortie, exist_ok=True)

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
            resultat = model.extract_entities_long(texte,{
            "personne": "Noms propres désignant des personnes physiques : prénoms, noms de famille, noms complets, surnoms et pseudonymes",
            "organisation": "Noms propres et sigles désignant des organismes publics ou privés, entreprises, universités, laboratoires, instituts, administrations et associations, INRS. Commence souvent par une majuscule ou est une acronyme.",
            "ville": "Noms propres de villes, communes et villages, uniquement lorsqu'ils désignent des lieux géographiques et non des établissements ou organisations",
            "pays": "Noms propres de pays et d'États souverains, exclusivement",
            "lieu": "Noms propres de quartiers, régions, départements, provinces et sites géographiques. Exclure les villes, pays et noms d'organisations",
            "origine": "Gentilés, nationalités et expressions désignant l'origine géographique ou nationale des personnes. Exclure les noms de pays seuls",
            "formation": "Noms de diplômes, cursus universitaires, niveaux et statuts d'études : doctorat, master, licence, DEA, doctorant, étudiant.",
            "métier": "Noms de professions, métiers, fonctions et postes professionnels. Exclure les diplômes et les niveaux d'études.",
            "âge": "Âge d'une personne exprimé en chiffres ou en lettres. Exclure les durées et périodes chronologiques",
            "date": "Dates calendaires, années et périodes temporelles explicites. Exclure les âges et durées"},
            chunk_size=256,
            chunk_overlap=64,
            batch_size=1,
            include_confidence=True,
            include_spans=True,
            overlap_policy="allow",)

            print(texte)
            print(resultat)

            resultats.append(f"{texte}\n{resultat}\n")

#annotation xml 

            texte_annoté = texte ##je reprends mon texte pour éviter de casser gliner qui utilise la variable texte
            positions = [] ## j'ai besoin de savoir où commence mes éléments à annoter et j'utilise donc include_spans (qui me permet de savoir quand entité démarre dans la phrase) et je l'introduit dans positions

            for cat, entités in resultat["entities"].items(): #exemple gliner : {'entities': {'person': [{'text': 'magistère', 'confidence': 0.7929778099060059, 'start': 10, 'end': 19}], 'location': []}}
                    for entité in entités:
                        if entité["text"].lower() in ["euh", "heu", "hum", "hm", "ben", "bah"]:
                            continue
                        balise = ET.Element(cat) ## https://docs.python.org/3/library/xml.etree.elementtree.html#building-xml-documents
                        balise.text = entité["text"] ## avec include_spans, entities devient un dictionnaire et plus un tuple, il faut que j'annote uniquement "text"
                        xml = ET.tostring(balise, encoding="unicode") ##permet de transformer les balises elementTree en string manipulables
                        positions.append((entité["start"], entité["end"], xml))# Source - https://stackoverflow.com/a/6304835  
                        
            for start, end, xml in sorted(positions, reverse=True):
                balise = ET.fromstring(xml)
                ouverture = f"<{balise.tag}>"
                fermeture = f"</{balise.tag}>"
                texte_annoté = texte_annoté[:end] + fermeture + texte_annoté[end:]
                texte_annoté = texte_annoté[:start] + ouverture + texte_annoté[start:]
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
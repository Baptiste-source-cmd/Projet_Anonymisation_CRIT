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
            "person": "Prénoms et noms de personnes physiques, y compris les prénoms seuls, rares ou peu fréquents, les noms de famille seuls, les surnoms et les pseudonymes, notamment après des expressions comme : 'je m'appelle', 'mon prénom est', 'moi c'est, je suis'",
            "location": "Noms propres de lieux géographiques, de régions, départements, provinces, territoires et zones géographiques précises, à l'exclusion des villes, des pays, des adresses postales, des noms communs et des expressions spatiales vagues",
            "organization": "Noms propres d'organisations, d'associations, d'administrations, d'institutions publiques, de syndicats, de fondations et d'organismes identifiables, à l'exclusion des noms génériques d'institutions, des entreprises et des universités classées séparément",
            "city": "Noms propres de villes, de communes, de villages et de localités identifiables, y compris les communes étrangères et les petites localités",
            "country": "Noms propres de pays et d'États souverains, y compris leurs dénominations officielles et leurs formes courantes",
            "origine": "Gentilés, noms et adjectifs désignant l'appartenance ou l'origine géographique, nationale ou régionale de personnes ou de groupes humains, au singulier comme au pluriel, au masculin comme au féminin, notamment après des expressions comme je suis, je suis d'origine, mes parents sont",
            "job": "Noms de métiers, de professions, d'emplois, de fonctions professionnelles et de postes occupés par une personne, y compris les métiers rares, les appellations familières, les formes féminines et masculines, notamment après je travaille comme, je suis, je fais, mon métier est, je travaille en tant que",
            "company": "Noms propres d'entreprises, de sociétés, de commerces, de marques commerciales et d'employeurs identifiables, notamment après je travaille chez, je suis employé par, dans l'entreprise, chez, à l'exclusion des noms génériques de secteurs d'activité",
            "university": "Noms propres d'universités, de facultés, de grandes écoles et d'établissements d'enseignement supérieur identifiables, y compris leurs sigles et abréviations, notamment après j'étudie à, j'ai étudié à, je suis diplômé de",
            "school": "Noms propres d'établissements scolaires, de collèges, de lycées et de centres de formation identifiables, à l'exclusion des universités et des noms génériques d'établissements",
            "age": "Âges de personnes exprimés en chiffres ou en lettres, notamment j'ai 25 ans, elle a vingt ans, à l'âge de 18 ans, âgé de 30 ans, ainsi que les mentions explicites de tranches d'âge comme la trentaine, à l'exclusion des durées et des nombres sans rapport avec l'âge",
            "date": "Dates calendaires, années, mois, jours, dates de naissance, dates de décès, périodes chronologiques et expressions temporelles précises, exprimées en chiffres ou en lettres, notamment le '12 mars 1998', en '2005', depuis 'septembre 2010', à l'exclusion des durées et des expressions temporelles vagues",
            "address": "Adresses postales précises, noms propres de rues, avenues, boulevards, places, numéros de rue, codes postaux et autres éléments permettant de localiser précisément un domicile ou un établissement, à l'exclusion des simples noms de villes et de pays",
            "email": "Adresses électroniques personnelles ou professionnelles complètes, contenant un identifiant, le symbole arobase et un nom de domaine",
            "phone": "Numéros de téléphone personnels ou professionnels, fixes ou mobiles, français ou internationaux, avec ou sans indicatif téléphonique, éventuellement séparés par des espaces ou des points",
            "diploma": "Noms et intitulés précis de diplômes, certifications, titres scolaires et universitaires, qualifications et niveaux de formation, notamment CAP, BEP, bac professionnel, licence, master, doctorat et BTS",
            "nationality": "gentilés comme maghrébins, et mentions explicites de nationalité ou de citoyenneté juridique, notamment nationalité française, citoyenneté espagnole, double nationalité, lorsque le texte désigne un statut juridique et non une simple origine géographique"},
            chunk_size=256,
            chunk_overlap=64,
            batch_size=1,
            include_confidence=True,
            include_spans=True)

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
            for start, end, xml in sorted(positions, reverse=True): ##avec les annotations, xml faisait bugger gliner en décalant les phrases, il a fallu trouver une solution : j'introduis une lecture inversée de positions pour supprimer la deuxième annotation à la volée
                if limite is None or end <= limite:
                    texte_annoté = (f"{texte_annoté[:start]}{xml}{texte_annoté[end:]}") # Source - https://stackoverflow.com/a/59965745 [end] renvoyait une erreur d'indexage, sans :, la séquence s'arrête pas après "end"
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
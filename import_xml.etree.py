import xml.etree.ElementTree as ET
import os
print(os.getcwd())

docs = os.listdir(os.getcwd()) ## https://stackoverflow.com/questions/18262293/how-to-open-every-file-in-a-folder
TEI = '{http://www.tei-c.org/ns/1.0}'
TXM = '{http://textometrie.org/1.0}'
for doc in docs:
    if doc.endswith(".xml"):
        print(doc)
        tree = ET.parse(doc)    # Parse (lit et analyse) le fichier XML
        root = tree.getroot()  # Cherche tous les éléments <u> du namespace TEI      
        # <u> correspond ici à une unité de parole 
        u = root.iter(TEI + "u")
        liste_1 = []
        for u_iter in u:
            liste_1.append(u_iter)
            if u_iter is not None:
                print(u_iter.attrib)

        with open("modifié.txt", "w", encoding="UTF-8") as f:
            for i in liste_1: 
                who = i.get("who") # Récupère l'attribut "who" du <u> # 
                start = i.get("start") # Récupère l'attribut "start" 
                end = i.get("end")  # Récupère l'attribut "end"
                code = i.get("code")  
                mots = []# Crée une liste vide pour stocker les mots
                for word in i.iter(TEI + "w"):  #Cherche tous les éléments <w> à l'intérieur du <u>, <w> représente ici un mot
                    w2 = word.find(TXM + "form")# Cherche dans chaque <w> un élément <form> 

                    
                    if w2 is None: # Vérifie que l'élément <form> existe
                        continue
                    mots.append(w2.text) # Récupère le texte contenu dans <form> et l'ajoute à la liste "mots"
                f.write(f"{who} {code} {start} {end} : {' '.join(mots)}\n")#
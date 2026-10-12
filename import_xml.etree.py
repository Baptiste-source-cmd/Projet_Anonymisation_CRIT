import xml.etree.ElementTree as ET
import os
print(os.getcwd())

docs = os.listdir(os.getcwd()) ## https://stackoverflow.com/questions/18262293/how-to-open-every-file-in-a-folder
TEI = '{http://www.tei-c.org/ns/1.0}'
TXM = '{http://textometrie.org/1.0}'
frpos = "ana[@type='#frpos']"
frlemma = "ana[@type='#frlemma']"
for doc in docs:
    if doc.endswith(".xml"):
        print(doc)
        tree = ET.parse(doc)    # Parse : lit et analyse le contenu du fichier XML
        root = tree.getroot()  # Cherche tous les éléments <u> du standard  TEI      
        # <u> correspond ici à une unité/tour de parole 
        u = root.iter(TEI + "u")
        liste_1 = []
        for u_iter in u:
            liste_1.append(u_iter)
            if u_iter is not None:
                print(u_iter.attrib)

        with open(doc.replace(".xml", ".tsv"), "w", encoding="UTF-8") as f:  # permet de changer l'extension xml en tsv et conserver le nom du fichier
            f.write("doc\tDate\tindex_u\twho\tcode\tstart\tend\tw_id\tlem\tPOS\tforme\n") # permet dd'écrire les colonnes en maintenant une tabulation conforme aux tsv
            for nb_tour_parole, i in enumerate(liste_1): #enumerate pour avoir le numéro du tour
                who = i.get("who") # Récupère l'attribut "who" du <u> cad son indentifiant
                start = i.get("start") # Récupière l'attribut "start"  qui signale le début du tour
                end = i.get("end")  # Récupère l'attribut "end" qui signale la fin du tour
                code = i.get("code")  #récupère l'attribut de l'individu
                date_enreg = i.get("date") ## pas sûr de pourquoi ça fonctionne, puisque c'est pas dans i, qui est l'exploretion de <u> avec u_iter, alors que <date> est dans <div> et <text>
                
                for word in i.iter(TEI + "w"):  #Cherche tous les éléments <w> à l'intérieur du <u>, <w> représente ici un mot
                    w = word.find(TXM + "form")# Cherche dans chaque <w> un élément <txm form> , form représente la balise du mot 
                    POs = word.find(TXM + frpos)  # Récupère l'attribut du POS qui n'est pas dans u, trouvé une méthode alternative ==>  https://stackoverflow.com/questions/222375/elementtree-xpath-select-element-based-on-attribute
                    lem = word.find(TXM + frlemma) # récupère l'attribut du lemme
                    word2 = word.get("id") 
                    
                    if POs is not None: # if suffit pas, element tree demande if is not none ## "Use specific 'len(elem)' or 'elem is not None' test instead. if POs:"
                        POs = POs.text
                    if lem is not None:
                        lem = lem.text
                    if w is not None:
                        w2 = w.text or ""

                    
                    f.write(f"{doc}\t{date_enreg}\t{nb_tour_parole}\t{who}\t{code}\t{start}\t{end}\t{word2}\t{lem}\t\t{POs}\t{w2}\n") ## même chose que pour les colonnes, sauf qu'on prend ici le contenu des strings, et pas le nom de la colonne
                    f.write("\n") # saute une ligne à chaque fin de u
                f.write("\n") # saute une ligne à chaque fin de u

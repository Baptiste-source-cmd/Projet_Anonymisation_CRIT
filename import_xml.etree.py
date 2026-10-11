import xml.etree.ElementTree as ET
import os
print(os.getcwd())

docs = os.listdir(os.getcwd()) ## https://stackoverflow.com/questions/18262293/how-to-open-every-file-in-a-folder

for doc in docs:
    if doc.endswith(".xml"):
            print(doc)
            tree = ET.parse(doc)
            root = tree.getroot()
            u = root.iter("{http://www.tei-c.org/ns/1.0}u")
    liste_1 = list(u)

    with open("doc.txt","w",encoding="UTF-8") as f:
        for i in liste_1:
            who = i.get("who")
            start = i.get("start")
            end = i.get("end")
            code = i.get("code")  

            mots = []

            for word in i.iter("{http://www.tei-c.org/ns/1.0}w"):
                w2 = word.find("{http://textometrie.org/1.0}form")

                if w2 is not None:
                    mots.append(w2.text)
            f.write(f"{who} {start} {end} : {' '.join(mots)}\n")
    break

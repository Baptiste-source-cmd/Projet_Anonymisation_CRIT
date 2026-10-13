# Projet_Anonymisation_CRIT

outils développés dans le cadre du projet CRIT

=======

## Objectif
-Extraire et normaliser un corpus ici de type XML au format TEI/TXM : retirer les annotations XML pour préparer les données à anonymiser et les exploiter dans un NER (reconnaissance d'entité nommée) et/ou du machine learning

-À noter que les données ne sont pas intégrées au commit : de par leur caractère confidentiel, elles sont stockées hors du dépôt.

## Outils/librairies 
https://docs.python.org/3/library/xml.etree.elementtree.html <== Document ElementTree

https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html <== Documentation Pandas

https://github.com/urchade/GLiNER <== Github GLINER

ElementTree ; permet la lecture et le parcours des documents XML à travers l'itération des balises
TSV : l'export des données en TXT rendait l'utilisation de pandas plus difficile, et il fallait une gestion des noms de colonnes pour GLINER
pandas et GLINER : envisagés comme second outils pour la détection des entité nommées des documents

## Utilisation du script

-Nous voulions pouvoir avoir un corpus nettoyé en vue d'une intégration dans un modèle de machine learning ou pour d'autres outils automatisés

### Version TSV

Fonctionne de façon similaire à la version TXT, sauf qu'au lieu de retirer les balises et de ne récupérer qsue le contenu des balises qui nous intéressent, on récupère une ligne colonne propre pour chaque document XML, et on lui applique le contenu des balises recherchées pour chaque ligne. La différence majeure est également le choix de traiter la ligne avec <w> et non <u> (soit le mot au lieu du tour), le tour est toujours marqué par une séparation '\n'

Les colonnes sont les suivantes; ==> exemples
* doc : donne le nom du document ==> exemple_de_nom.xml
* date : donne la date de l'enregistrement ==> 12/07/25
* index_u : compte le tour de parole (à noter que les tours vides sont ignorés) ==> 5
* who : identifiant de l'individu s'exprimant ==> témoin ou ch_(initiales nom_personne)
* code : le nom de l'individu ==> George
* start et end : début et fin de tour de parole en timecode ==> 2.9200000000	4.1430000000
* w_id : balise d'identification du mot dans le document ==> exemple_de_nom_1.xml (= première balise <w>)
* lem : le lemme du mot dans <w> ==> mangent : manger
* POS : la catégorie morpho-syntaxique du mot dans <w> ==> manger : Verbe
* w2 (= <txm:form>) : le contenu de la balise texte ==> mangent
### Version TXT
-Le script permet donc de retirer l'ensemble des balises, et de ne conserver que le texte, à cela s'ajoute le contenu de quelques autres balises, les balises de timecode, la balise qui permet de savoir qui parle, et la balise du code de l'individu, cela donne une ligne qui ressemble à :

-"Who" "Code" "Début" "Fin du tour": "texte"

-exemple : Témoin Pierre 55.45000000 57.9999000000 : le corpus est dexmlisé

## État d'avancement actuel
- [x] Extraction des tours de parole depuis les XML TEI
- [x] Traitement de l'ensemble des documents en une seule fois
- [x] code test en txt transformé pour que le xml se change en .tsv
- [x] Rajout des informations grammaticales et date
- [ ] Structuration avec pandas
- [ ] Application d'un tsv avec GLINER
- ==> Remise des balises d'entités nommées : abandonné, les balises ne sont pas assez bien annotées

## Auteurs
Développé par mes collègues de travail et moi-même dans cadre d'un projet universitaire d'anonymisation de données.

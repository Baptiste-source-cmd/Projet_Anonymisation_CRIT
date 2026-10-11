# Projet d'anonymisation CRIT (corpus CEM-TXM)
outils développés dans le cadre du projet CRIT

Premier outil développé autour de la bibliothèque Python Element Tree pour retirer les balises XML du corpus proprement sur l'ensemble du corpus.

https://docs.python.org/3/library/xml.etree.elementtree.html
## Objectif
-Extraire et normaliser un corpus ici de type XML au format TEI/TXM : retirer les annotations XML pour préparer les données à anonymiser
-À noter que les données ne sont pas intégrées au commit : de par leur caractère confidentiel, elles sont stockées hors du dépôt.

## Utilisation
-Nous voulions pouvoir avoir un corpus nettoyé en vue d'une intégration dans un modèle de machine learning ou pour d'autres outils automatisés

-Le script permet donc de retirer l'ensemble des balises, et de ne conserver que le texte, à cela s'ajoute le contenu de quelques autres balises, les balises de timecode, la balise qui permet de savoir qui parle, et la balise du code de l'individu, cela donne une ligne qui ressemble à :

-"Who" "Code" "Début" "Fin du tour": "texte"
-exemple : Témoin Pierre 55.45000000 57.9999000000 : le corpus est dexmlisé

## État d'avancement actuel
- [x] Extraction des interventions depuis les XML TEI
- [ ] Traitement de l'ensemble des documents en une seule passe (à corriger : éviter que chaque fichier écrase la sortie précédente)
- [ ] Remise des balises d'entités nommées

## Auteurs
Développé par moi-même et mes collègues de travail dans cadre d'un projet universitaire d'anonymisation de données.

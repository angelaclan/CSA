# Opérations sur le graphe de flot de controle [1 séance]

Dans ce TP, vous allez réaliser des opérations sur le graphe de flot de
contrôle. Pour ce faire, vous allez travailler avec LLVMLite, un plugin
python qui permet de travailler avec la représentation intermédiaire (IR) de
LLVM, a partir du langage python. 

## Prérequis
 * Python 3.7 (et pas une autre version de 3.X)
 * Clang
 * Graphviz (optionnel)

## Préparation

Clonez le dépot à l'adresse {{TODO_REPO_LLVMLITE_TP}}, et compilez l'exemple
(dans le sous-dossier example/) avec "make". 
Si tout se passe bien, vous devriez avoir le message "Test OK".
Pour commencer à travailler, vous pouvez faire une copie du dossier "example"
vers le nom de votre choix (par exemple "tp1") en faisant:

```
cp -a example tp1
``` 

## Examiner le code source

Examinez le source `analysis.py` et le `Makefile`.

Un squelette d'analyse est disponible dans `analysis.py`, celui ci contient les
instructions nécessaires au chargement d'un fichier bitcode contenant l'IR LLVM
(produit par clang a partir du source C du programme à analyser), et
construction d'un CFG (exporté au format dot et convertissable en pdf). Le
fichier donne des exemples de parcours du CFG, des blocs de base, et des
instructions dans les blocs de base.


Le fichier "Makefile" contient tout ce qu'il faut pour compiler le fichier source C
en bitcode IR LLVM, lancer l'analyse dessus, et peut également sortir le CFG au format
PDF.

## Parcours du CFG

Vous réaliserez les exercices dans le fichier `analysis.py` (bien entendu, rien ne vous empeche
de créer des modules python dans d'autres fichiers, et de les appeler depuis `analysis.py`).

Réalisez tout d'abord une fonction permettant de vérifier que le CFG est connexe et que chaque
bloc est atteignable. Vous testerez ensuite la fonction avec le programme C d'exemple. 

## Domination

En utilisant l'algorithme de votre choix (par ex: l'algorithme de Kildall),
développez une fonction qui réalise le calcul de la relation de domination
entre chaque blocs de base. 

Question: soit 3 blocs de base bb1, bb2, et bb3, tel que bb2 domine bb3, et bb1 domine bb3.
Est-il possible que ni bb2 ne domine bb1, ni bb1 ne domine bb2 ? Pourquoi ? 

En fonction de la réponse à la question précédente: quelle est la structure de donnée qu'il faudrait
utiliser pour représenter l'ensemble des relations de dominations dans le CFG? Réalisez une fonction
qui génère cette structure de données.

Testez tout ceci sur le programme C d'exemple.

## Boucles 

En utilisant les informations récupérées dans l'exercice précédent, réalisez une fonction qui va détecter
les boucles présentes dans le programme, et identifier leurs headers et back-edge (on se limitera aux
boucles bien formées, ayant un unique header). 

Ensuite, en utilisant la méthode de votre choix, réalisez une calculez
l'information d'appartenance des blocs de bases aux boucles. 

A partir de ces informations, développez une fonction qui reconstitue un arbre de hierarchie des boucles
(chaque noeud représente une boucle, et les fils d'un noeud représentent les boucles imbriquées).

Testez tout ceci sur le programme C d'exemple.

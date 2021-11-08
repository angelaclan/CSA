# Interprétation abstraite avec domaine relationel [2 séances]

Dans ce TP, vous allez réaliser une analyse un peu plus poussée,
toujours avec de l'IR LLVM. En plus de LLVMLite et Python, vous
aurez besoin également du module pplpy, permettant de s'interfacer
avec la bibliothèque PPL (Parma Polyhedra Library).

## Prérequis
 * Python 3.7 (et pas une autre version de 3.X)
 * Clang
 * pplpy
 * PPL
 * Graphviz (optionnel)


## Préparation

Vous allez pouvoir récuperer l'essentiel du code du TP2. 
Vous pouvez copier votre dossier du TP2 et lui donner le
nom de votre choix (par exemple, "tp3").

Vous allez seulement modifier les fonctions de transfert,
de join, de widening, et la définition du domaine abstrait
(avec les élements Top et Bottom).

## Travail à réaliser

### Définition du problème

L'analyse par intervalle définie dans le TP précédent n'a
pas un domaine relationnel. C'est-à-dire que si nous avons,
par exemple, un programme de la sorte:
```
a = rand(0,10);
b = a;
c = a - b;
```

on pourra déterminer que a et b sont dans l'intervalle
[0,10], mais pas que a == b. Ansi, l'intervalle pour c
sera [-10, 10], ce qui est pessimiste (en effet, si on
se rends compte que a == b, on sait que c == 0).

Pour résoudre ce probleme, nous allons développer une
analyse qui représente l'ensemble des valeurs possibles
des variables par un système de contraintes linéaires
(ou, de manière équivalente, par un polyèdre).

Pour ceci, nous allons utiliser le module pplpy, qui
sert d'interface à la bibliothèque PPL, servant à 
manipuler des polyèdres.

#### Domaine concret

Quel est le domaine concret permettant de représenter
l'état du programme? Est-ce que c'est le même que
pour le TP2?

#### Domaine abstrait 

Proposez une définition de domaine abstrait qui permette
de représenter les relations linéaires entre les variables
du programme.

Donnez une expression (par exemple, sous forme d'ensembles
de contraintes linéaires) de l'état Top et de l'état Bottom?

#### Fonctions d'abstraction et de concrétisation

Proposez des définitions (mathématiques, il n'y a pas de code à faire) de
fonctions d'abstraction (permettant de passer d'un élement de C à un
ensemble d'élements de A), et une fonction de concrétisation (permettant
de passer d'un élement de A à un ensemble d'élements de C)

#### Ordre, et join

Retrouvez dans la documentation de la PPL les fonctions qui vont vous
permettre de réaliser le test d'inclusion et l'enveloppe convexe 
sur les polyèdres.

En déduire une fonction de comparaison, et une fonction de Join pour
vos états abstraits.

#### Opérations arithmétiques et logiques

Dans le cas d'opérations arithmétiques exprimables
par une relation linéaire (ex: addition), leur
fonction de transfert pourra correspondre à un
ajout de contraintes linéaires dans le polyèdre
associé à l'état abstrait. 

Quelles sont les opérations pour lesquelles
il n'est pas possible de faire cela ?
Est-il possible de s'en sortir dans ce cas la?
Comment? 

### Implémentation

Implémentez ces fonctions dans votre analyse, et 
testez la sur quelques programmes qui permettront
de mettre en évidence l'avantage apporté par
une analyse à domaine relationnel.

### Améliorations

#### Widening

En regardant la documentation de la PPL, trouvez une 
fonction qui va vous aider à créer un opérateur
de widening, puis implémentez ceci dans votre analyse,
et testez le sur un programme (de préférence, sur un programme
que vous n'arriviez pas à analyser sans opérateur de widening)

#### Filtering 

Sur quels types de conditions pourrez-vous implémenter le filtering
dans votre analyse? 

Implémentez le filtering pour les types de conditions où c'est possible,
puis testez le avec un programme comportant des conditions.

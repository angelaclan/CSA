# Interprétation abstraite avec domaine non-relationel [2 séances]

Dans ce TP, vous allez réaliser une analyse simple basée sur de l'interprétation
abstraite sur de l'IR LLVM. Pour ce faire, vous utiliserez encore LLVMLite et Python.
Dans ce TP, vous allez réaliser des opérations sur le graphe de flot de
contrôle. Pour ce faire, vous allez travailler avec LLVMLite, un plugin
python qui permet de travailler avec la représentation intermédiaire (IR) de
LLVM, a partir du langage python.

## Prérequis
 * Python 3.7 (et pas une autre version de 3.X)
 * Clang
 * Graphviz (optionnel)

## Préparation

Vous allez pouvoir partir du même projet que pour le TP1.

Pour commencer à travailler, vous pouvez faire une copie du dossier "example"
vers le nom de votre choix (par exemple "tp2") en faisant:

```
cp -a example tp2
```

## Travail à réaliser

### Définition du problème

On se propose de réaliser une analyse qui permettra de trouver les intervalles
possibles de valeurs des variables de notre programme. Le programme est sous
forme d'IR LLVM. 

#### Domaine concret

Proposez une définition formelle d'un domaine concret C permettant de représenter
l'état d'un programme.

#### Domaine abstrait 

Proposez un domaine abstrait A qui permette de représenter les intervalles
des valeurs possibles du programme.

Également, quels sont les élements Top et Bottom de ce domaine abstrait?

#### Fonctions d'abstraction et de concrétisation

Proposez des définitions (mathématiques, il n'y a pas de code à faire) de
fonctions d'abstraction (permettant de passer d'un élement de C à un
ensemble d'élements de A), et une fonction de concrétisation (permettant
de passer d'un élement de A à un ensemble d'élements de C)

#### Ordre, et join

Comment comparer deux états abstraits ? Un état abstrait a1
est "plus petit" qu'un état abstrait a2, si la concrétisation de a1
est inclue dans la concrétisation de a2.

Soient deux états abstraits a1 et a2. Le résultat a3 = Join(a1, a2)
devrait être le plus petit état abstrait possible, tel que a1 et
a2 sont tous les deux plus petits que a3.

Donnez une formulation possible de votre Join.

#### Opérations arithmétiques et logiques

Il faut maintenant donner les fonctions de transfert pour chaque
opération arithmétique utilisable dans le programme.

Pour chaque opération arithmétique, une fonction de transfert correspondante
doit calculer l'état abstrait après l'opération, en fonction de l'état abstrait
avant l'opération, et des opérandes.

### Implémentation

Implémentez en python les fonctions préparées ci-dessus.

Pour votre analyse, vous n'avez besoin d'implémenter que les opérateurs
sur le domaine abstrait, à savoir: le Join, et les fonctions de transferts
des différentes opérations.

Testez l'implémentation de vos fonctions avec quelques petits exemples
avant de passer à la suite.

#### Itération chaotique

Le principe de l'itération chaotique est, tout d'abord, d'associer
un état abstrait à chaque point du programme, c'est à dire avant
et après chaque instruction. La valeur initiale de cet état
abstrait sera Bottom pour tous les points du programme, sauf
pour le point d'entrée, pour lequel l'état abstrai sera Top. 

Implémentez tout d'abord un moyen de stocker un état abstrait
pour chaque point du programme, et de le modifier.

Ensuite, il faut faire évoluer les états abstraits à chaque
point du programme, jusqu'a obtenir une convergence vers un
point fixe, par l'application de ces fonctions:
 * La fonction de transfert associée à une instruction permet d'obtenir l'état abstrait après l'instruction, en fonction de l'état abstrait d'avant l'instruction
 * En cas d'instructions ayant plusieurs prédécesseurs: la fonction join permet d'obtenir l'état abstrait avant une instruction, en fonction des états abstraits après chaque instruction prédécesseur.

Implémentez une boucle qui réalise ceci jusqu'à obtenir une
convergence vers un point fixe (c'est-à-dire que quelque
soit l'application de fonctions de transfert ou de join,
il n'est plus possible de modifier les états abstraits).

Est-ce que l'ordre dans lequel vous réalisez vos
applications de fonctions de transfert ou de join
modifie le résultat? Ou le temps d'analyse?

### Améliorations

Il est possible de faire diverses améliorations au niveau
de la précision de l'analyse, et du temps de calcul.

#### Widening

Pour l'instant, vous n'avez pas encore d'opérateur de
widening. Quelles sont les conséquences? Est-ce que
vous pouvez créer un programme à analyser, de telle
sorte que votre analyse ne se termine pas ?

Une fois ceci fait, vous allez implémenter un opérateur
de widening. Vous pouvez trouver un opérateur de widening
sur les intervalles dans votre cours. 

A quel moment il faut utiliser l'opérateur de widening? 
(Vous aurez peut-être besoin des informations sur
les boucles, en vous aidant des analyses réalisées
lors du TP précédent...)

Intégrez votre opérateur de widening dans votre analyse,
essayez à nouveau d'analyser le programme qui empechait
votre analyse de se terminer.

#### Tri topologique

Dans la partie "Itération chaotique", vous avez certainement
remarqué que l'ordre dans lequel vous appliquez vos fonctions
va influencer le temps d'analyse. 

Une stratégie acceptable peut-être de réaliser un tri topologique des noeuds du
CFG (en ignorant les arc-retour de boucle). Ensuite, lors de l'analyse, on
pourra traiter les noeuds par ordre topologique. 

On prendra soin également de ne traiter un noeud que si son
état abstrait précédent a changé.

A votre avis, pourquoi cette stratégie fonctionne? 

Question ouverte: Est-ce vous pouvez trouver un moyen pour améliorer
encore le temps d'analyse en modifiant l'ordre ?

#### Filtering 

Soit un programme du genre: 

```
if (x > 10) {
}
```

Que peut-on dire sur les valeurs possibles de `x` à l'interieur du if ? 

Pour l'instant, votre analyse ne permet pas de découvrir cette propriété. 

Pour qu'elle puisse le faire, il faudrait réaliser une fonction de transfert
pour les branchements conditionnels, de telle sorte que l'état abstrait renvoyé
prenne en compte la condition. Cette approche s'appelle le Filtering.

Implémentez ceci dans votre analyse.


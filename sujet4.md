# Tests et fuzzing [1 séance]

## Prérequis
 * Une version récente de Clang/LLVM (version 9 OK)
 * Python 3

## Préparation
Clonez le dépot à l'adresse {{DEPOT_PROG_MAL_CODE}}, et 
compilez le avec `make` 

## Description du programme cible

Ce programme prends en entrée standard des données au format PCAP
(https://wiki.wireshark.org/Development/LibpcapFileFormat), ceci est un format
de capture de paquets réseau utilisé notamment par Wireshark et tcpdump. Le
programme affiche ensuite des informations sur les paquets, tels que les IPs,
et le contenu des données des "pings".

## Experimentation

Experimentez avec le programme: vous pouvez par exemple faire quelques captures
réseau au format PCAP avec wireshark ou tcpdump. Exemple avec tcpdump:

```
tcpdump -i <interface reseau> -w fichier.pcap
```

Il y a aussi des fichiers pcap d'exemple fournis dans le dépot. 

Vous pouvez lancer le programme en donnant le fichier pcap en entrée standard
pour voir ce qu'il se passe.

## Analyse du programme

Ce programme comporte une faille de sécurité de gestion mémoire. Si vous êtes à
l'aise avec ce sujet, compte tenu de la taille réduite du programme vous
pourriez peut-être trouver le bug en lisant simplement le code source.

Toutefois, le but de l'exercice est de se familiariser avec les techniques
permettant de trouver automatiquement les problèmes dans un programme.

Pour ce faire, vous allez d'abord développer vous-même un petit fuzzer aléatoire,
et ensuite vous essayerez le fuzzer intégré dans LLVM (libFuzz).

## Développement d'un fuzzer aléatoire

Le sujet du TP vous guidera dans le développement en langage C, mais vous
pouvez développer dans le langage de votre choix tant que les objectifs sont
atteints.

### Lancer un processus fils

Faites un programme qui lance le programme vulnérable en tant que processus
fils. (indice: `man 3 execl` et `man 2 fork`)

Comment récuperer son status de sortie? Comment savoir s'il a planté à cause
d'une erreur mémoire? (indice: `man 2 wait`)

### Rediriger l'entrée standard

Comment rediriger l'entrée standard du programme vulnérable pour pouvoir lui
envoyer ce qu'on veut? (indice: `man 2 pipe` et `man 2 dup`)

Modifiez votre programme pour qu'il passe un contenu quelconque (que vous
pourrez préparer dans un tableau de char, après l'avoir lu depuis un fichier
donné en paramètre) en tant qu'entrée standard au programme vulnérable.

### Randomiser l'entrée du programme

A partir de ce que vous avez réalisé dans les étapes ci-dessous, vous allez
terminer votre outil de fuzzing.

Préparez d'abord un fichier d'entrée valide au format pcap, contenant un paquet
ICMP echo (ping). Un exemple est fourni dans le dépot git.

Ensuite, faites en sorte que votre programme de fuzzing lance le programme
vulnérable, en lui envoyant (via l'entrée standard) votre fichier d'entrée
valide, qui sera au préalable modifiée de manière aléatoire. 

Exemples de modifications aléatoires que vous pouvez réaliser:
 * Inverser des bits au hasard: pour P fixé entre 0 et 1, chaque bit du fichier d'entrée pourra être inversé avec une probabilité de P (ou laissé tel quel avec une probabilité de 1-P)
 * Modifier un certain nombre d'octets au au hasard: pour P fixé entre 0 et 1, chaque octet du fichier pourra être remplacé par une valeur aléatoire avec une probabilité de P (ou laissé tel quel avec une probabilité de 1-P)

## Utilisation de libFuzz

LibFuzz est un outil de fuzzing guidé, livré avec Clang. Il permet de fuzzer un
programme en s'aidant d'instrumentation pour aider à la génération de jeux de
tests avec la couverture la plus importante possible. Il peut fonctionner à
partir d'un jeu de test initial fourni par l'utilisateur, ou bien de manière
totalement autonome. 

Pour fonctionner correctement, libFuzz a besoin que le programme cible soit
compilé avec des flags qui permettent l'instrumentation:

```
-fsanitize=fuzzer
```

Pour plus d'efficacité, il est aussi recommandé d'activer ASan, UBSan, les
symboles de debug, ainsi que de désactiver les optimisations.

```
-fsanitize=fuzzer,address,undefined -O0 -g
```

De plus, il faudra enlever (ou commenter!) le `main()` du programme (en effet,
celui sera fourni automatiquement par libFuzz), et à la place créer une
fonction de prototype suivant:

```
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size);
```

Cette fonction sera appelée automatiquement par libFuzz pour chaque entrée à tester,
les données de l'entrée seront fournies dans `Data` et sa taille en octets dans `Size`.
Il appartient alors à cette fonction `LLVMFuzzerTestOneInput` d'utiliser les données
fournies pour lancer un test sur le programme vulnérable.

La génération des jeux de tests et la détection des erreurs (crashs, ...) résultantes
est réalisée automatiquement par libFuzz.


### Adapter le Makefile 

Préparer une cible du `Makefile` qui compile le programme vulnérable avec les
options nécessaires pour libFuzz. Lors de l'utilisation de cette cible, il
faudra éviter de déclarer/définir la fonction `main()`, vous pouvez utiliser
des techniques de préprocesseur et/ou de compilation séparée pour cela. 

Il vous faudra aussi définir la fonction LLVMFuzzerTestOneInput (que vous
pouvez laisser vide pour l'instant), il vous est conseillé de la définir dans
une autre unité de compilation.

### Créer le contenu de la fonction LLVMFuzzerTestOneInput

La fonction LLVMFuzzerTestOneInput prends ses données dans un buffer, mais le programme
vulnérable les accepte sur l'entrée standard, via un stream. Vous ne pouvez pas utiliser
de pipe comme dans l'exercice sur le fuzzing aléatoire, étant donné que votre fonction
LLVMFuzzerTestOneInput se situe dans le meme process que le programme vulnérable.

Pour vous en sortir, vous pouvez regarder la documentation de la classe
suivante de la bibliothèque standard C++:

```
std::istringstream
```

### Expérimentation avec votre fuzzer


Lancez le fichier executable de votre fuzzer avec l'option `-help=1` pour voir
la liste des options en ligne de commande.  Comment faire pour passer un
dossier contenant un jeu de test? 

Préparez un dossier d'entrée contenant au moins un fichier pcap valide (par
exemple, le meme que celui que vous avez utilisé avec le fuzzing aléatoire), et
lancez votre fuzzer basé sur libFuzz avec ce dossier.

En combien de temps le fuzzer va-t'il trouver une entrée faisant crasher le
programme vulnérable? Comparez ceci aux résultats que vous avez eu avec le
fuzzer aléatoire.

Essayez maintenant de lancer le fuzzer sans aucun dossier de jeu de test.


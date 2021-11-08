# Squelette pour utilisation de LLVMLite

## Prérequis
 * Python 3.7 (et pas une autre version de 3.X)
 * Clang
 * Graphviz (optionnel)

## Contenu du dossier

 * `llvmlite/` bindings python pour LLVM
 * `example/` exemple d'analyseur qui calcule la relation de dominance entre basic blocks sur un programme simple.
   (le fichier `analysis.py` contient l'analyseur lui-même, alors que
   `cfg_helper.py` est un petit module d'aide à la navigation dans le CFG)

Utilisation de l'exemple (en ayant python3.7 dans votre PATH):

```
cd example/
make
```

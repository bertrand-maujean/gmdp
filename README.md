# gmdp - Générateur de Mots de Passe
Eh oui, encore un. Voici pourquoi c'est le meilleur générateur de mots de passe :

- le mode "smart4" consiste à générer des blocs de 4 caractères consécutifs de la même classe (maj, min, chiffres, ponctu). Du coup, il devient facile de distinguer un O d'un 0, un l d'un 1... Par ailleurs, pour saisir les MdP sur un smartphone, on zappe moins de table de clavier sur le clavier virtuel
- le mode "bip39" permet lui d'utiliser des blocs de 4 lettres selon la recommandation "Bitcoin Improvement Proposal 39". Ce document à pour objet de proposer une méthode pour avoir des MdP plus facile à retenir.
- L'espace des possibles dans lequel le mot de passe est choisi est évalué par son log2 (son "entropie" comme on dit souvent dans le domaine). Le calcul tient compte de la réalité du mode choisi.
- La longueur du MdP n'est pas exprimée en nombre de caractères, mais justement, par ce nombre de bits



-----------------------
# Compilation / installation
C'est un simple script python3 à poser là où vous voulez (/usr/local/bin pour que tout le monde puisse l'utiliser).
Pour le mode "bip39", il faut charger des dictionnaires, le programme suppose que le dictionnaire par défaut est :
```
/usr/share/dict/bip39/french.txt
```
Donc pas de package, pas de setup.exe

-----------------------
# Options
- vous utiliserez certainement le mode "--brief" qui affiche un MdP par ligne
- --many permet d'en générer plusieurs
- Sinon, le format de sortie en json permet de connaitre l' "entropie" effectivement générée, et pour le mode bip39, les mots complets pour se souvenir.
 

-----------------------
# Idées pour le futur
- Mode qui n'utilise que des caractères compatibles Azerty - Qwerty

-----------------------
# Licence
This program is released under the terms of the GNU GPLv3 License.
It comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
See LICENSE.txt file


#!/usr/bin/env python3
#coding: utf-8

"""
    gmdp.py Générateur de Mots de Passe
    Copyright (C) 2021 Bertrand MAUJEAN

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    See LICENSE.txt along with this program
    or <https://www.gnu.org/licenses/>.
"""

import argparse
import random
import math
import time
import unicodedata
import json



# https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki


majus = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
minus = set("abcdefghijklmnopqrstuvwxyz")
digit = set("0123456789")
ponct = set("!@#$%^&*()-_+=~[]{}|:;\<>,.?/")
charClass = {"u": majus, "l":minus, "d":digit, "p":ponct}





# ****************************************
# Renvoie à quelle classe appartient un caractère
def getCharClass(c):
    for l in set("uldp"):
        if c in charClass[l]:
            return l
        
    return None




# ****************************************
# Génération d'un MdP simple avec smart4
# Si ponctuation : blocs de 4x{U, L, D} avec des P entre
# Si pas ponctuation : blocs de 4x{U,L,D}, avec pas deux classes qui se suivent
def genereMdpSmart4(bits_, chars_, bip39dict=None):
    result = ""              # MdP en cours de génération
    bits=0.0                 # Qté d'information contenue 
    charsEffectifs = set()   # ensemble des classes de caractères représentées
    universe = set()
    bip39mots = []
 
    premier=True
    dejaD  =False # si les "d" sont passés
    clPrec =set() # classe du bloc précédent 
    while ((bits<bits_) or (chars_ != charsEffectifs)): # tant que pas assez de bits, et que toutes les classes de caractères ne sont pas passées
        
        if ("p" in chars_) and not premier:
            c       = random.choice(list(ponct)) 
            result += c
            bits   += math.log2(len(ponct))
            charsEffectifs.add("p")

        if chars_ == charsEffectifs:
            if dejaD:
                cl = random.choice(list(chars_ - set("pd") - clPrec))
            else:
                cl = random.choice(list(chars_ - set("p")  - clPrec))

        else:
            cl = random.choice(list(chars_ - set("p") - charsEffectifs - clPrec))

        if (bip39dict) and (cl != "d"):
            n = random.randrange(2048)
            bip39mots.append(bip39dict[n])
            
            if cl == "u":
                result += bip39dict[n][0:4].upper()
            else:
                result += bip39dict[n][0:4].lower()
                       
            bits += 11

        else:
            
            for k in range(4):
                c       = random.choice(list(charClass[cl])) 
                result += c
                bits   += math.log2(len(charClass[cl]))

        if cl == "d":
            dejaD = True

        clPrec = set(cl)

        premier=False            
        charsEffectifs.add(cl)

    result = {"mdp":result,  "bits":bits }
    if bip39dict:
        result.update ( { "mnemo": bip39mots } )
            

    return result 



# ****************************************
# Génération d'un MdP simple sans smart4
def genereMdp(bits_, chars_):
    
    result = ""              # MdP en cours de génération
    bits=0.0                 # Qté d'information contenue 
    charsEffectifs = set()   # ensemble des classes de caractères représentées
    universe = set()
    for l in chars_:
        universe |= charClass[l]
        
    while ((bits<bits_) or (chars_  != charsEffectifs)): # tant que pas assez de bits, et que toutes les classes de caractères ne sont pas passées
        c       = random.choice(list(universe)) 
        result += c
        bits   += math.log2(len(universe))
        charsEffectifs.add(getCharClass(c))

    result = {"mdp":result,  "bits":bits }
    return result


helpDescription="""
Génère des mots de passe astucieux :
- l'entropie (= log2 du cardinal de l'ensemble des MdP possibles) est calculée réellement
- on ne spécifie pas le nombre de caractères, mais le minimum d' 'entropie' en bits
  (défaut 70)
- le mode "bip39" consiste à utiliser les listes de mots de la
  "Bitcoin Improvement Proposal 39"
  voir : https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
- en mode bip39, si affichage json (= pas --brief), les mots clés sont donnés
  pour la mémorisation
- le mode "smart4" consiste à générer des blocs de 4 caractères consécutifs,
  tous de la même classe de caractères. Ceci évite de zapper sur les claviers
  virtuels de smartphones

Notes :
- le calcul de l'entropie est réel :
  - Un bloc de 4 en "u" (uppercase) seulement compte pour log2(26**4)
  - Un bloc "bip39" compte pour 11 bits = log2(2048)
    (normalement 12, car upper/lower, mais pas pris en compte ici)

- Un MdP 12 caractères upper/lower /digit/ponctuation,
  totalement aléatoire, a une 'entropie' de :
  log2[ (26+26+10+25)**12 ] = 77 bits
  (pour fixer les idées)

- l'initialisation du PRNG est celle prévue localement par python3
  
"""


helpEpilog = """
Exemples :

./gmdp.py
Génère un MdP de 70 bits au moins, en mode smart4 par défaut


./gmdp.py --raw --chars=uld --brief --many=10
Génère une liste de 10 MdP de 70 bits au moins, en mode "raw" (= pas smart),
avec majuscules, minuscules, chiffres, affiché en mode court un par ligne

Comparaison : en mode bip39, les MdP sont un peu plus longs
pour une 'entropie' donnée :
./gmdp.py --chars=uld --brief
./gmdp.py --chars=uld --bip39 --brief

"""


# ****************************************
# Programme principal
def main():
    
    # Parse les arguments  en ligne de commande
    parser = argparse.ArgumentParser(description = helpDescription, epilog=helpEpilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--raw",        default=True,     dest="smart4",   action='store_false', help="Format à utiliser : désactive le mode 'smart4' ")
    parser.add_argument("--bip39",      default=False,    dest="bip39",    action="store_true",  help="Utilise la liste de mots BIP39 pour les blocs de 4 lettres")
    parser.add_argument("--bip39lst",   default="/usr/share/dict/bip39/french.txt", dest="bip39lst", help="Liste bip39 à utiliser  (défaut : /usr/share/dict/bip39/french.txt)")
    parser.add_argument("--brief",      default=False,    dest="brief",    action="store_true",  help="Affiche uniquement les MdP, un par ligne (défaut : json avec toutes les infos)")
    parser.add_argument("--bits",       default="70",     dest="bits",                           help="Nombre de bits minimum ('entropie', 70 bits par défaut)")
    parser.add_argument("--chars",      default="ludp",   dest="chars",                          help="Caractères à utiliser (l=lower, u=upper, d=digit, p=ponctuation)")
    parser.add_argument("--many",       default=1,        dest="many",                           help="nb de MdP a générer")
    #parser.add_argument("--qwazerty",   default=False,    dest="qwazerty", action='store_true',  help="Uniquement des caractères compatibles entre Qwerty et Azerty")
    #parser.add_argument("--spell",      default=False,    dest="spell",    action='store_true',  help="Alterne consonnes/voyelles")        
    args = parser.parse_args()
    args.chars = set(args.chars)
    args.many = int(args.many)
    args.bits = float(args.bits)
        
    # Vérifie les bêtises
    if args.bip39 and len(args.chars)<2:
        print("Pour le mode bip39, sélectionner plutôt chars=ul au moins")
        return
    
    if args.smart4 and len(args.chars)<2:
        print("Pour le mode bip39, sélectionner plutôt chars=ul au moins")
        return

    if args.bits < 40:
        args.bits = 40.0
        
    if args.bits > 1024:
        args.bits = 1024.0
        

    # Lit éventuellement une liste bip39
    bip39dict=None
    if args.bip39:
        bip39dict=[]
        try:
            f=open(args.bip39lst, "rt", encoding="utf-8")
            l=f.readline()
            while (l):
                l=l.strip("\n")
                l = ''.join((c for c in unicodedata.normalize('NFD', l) if unicodedata.category(c) != 'Mn'))
                bip39dict.append(l)
                l=f.readline()
            f.close()
            
        except Exception as e:
            print("Erreur en accédant au fichier {:s}".format(args.bip39lst))
            print(str(e))
            return
        
        if len(bip39dict) != 2048:
            print("Erreur : la longuur du dictionnaire BIP39 indiqué n'est pas 2048")
            return


    # génère les MdP
    mdps=[]
    for n in range(args.many):
        if args.bip39 or args.smart4:
            mdps.append( genereMdpSmart4(args.bits, args.chars, bip39dict=bip39dict) )
        else:
            mdps.append ( genereMdp(args.bits, args.chars) )


    if args.brief:
        for m in mdps:
            print(m["mdp"])
    else:
        print(json.dumps(mdps, indent=3))

                  

    return



if __name__ == "__main__":
    main()
else:
    print("Ce programme n'est pas fait pour être importé comme module")

    

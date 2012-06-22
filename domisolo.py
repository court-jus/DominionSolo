#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

USAGE = """
###############################################################################
                                 Dominion Solo
###############################################################################

Introduction
============

Bienvenue dans cette aide de jeu pour Dominion permettant de jouer en
solitaire. Cette variante a été créée par Bastien Nemett et est disponible ici:
http://www.trictrac.net/jeux/forum/viewtopic.php?p=1334034

Le but du jeu est d'obtenir, en 20 tours de jeu, plus de point qu'une province
choisie en début de partie (les cartes "Conquête")

Sélectionnez de la façon qui vous plaira les 10 cartes royaumes avec lesquelles
vous jouerez.

Au début de chaque tour de jeu, un évènement vous sera présenté. Celui-ci
influencera vos différentes phases du jeu.

A la fin de chaque tour de jeu, le temps passe. Vous avez 20 tours avant la fin
de la partie.

Quelques ajustement des cartes Action/Attaque et Action/Réaction
================================================================

Sorcière : Piochez 2 cartes + Posez une carte malédiction sur la carte
"Conquête" que vous avez choisie

Milice : +2 pièces / Avancez le marqueur "Armée" d'une case sur la carte
conquête

Voleur : Prenez 1 cuivre / Avancez le marqueur "Trésor" d'une case sur la carte
conquête

Espion : Regardez la carte du sommet de votre deck. Choisissez si vous la
défaussez ou non + Avancez le marqueur "Armée" d'une case sur la carte conquête

Bureaucrate : Recevez 1 argent / Avancez le marqueur "Trésor" d'une case sur la
carte conquête

A chaque fois qu'un marqueur "Armée" ou "Trésor" atteint la dernière case de sa
piste sur la carte "conquête", posez une carte malédiction sur la carte
conquête et remettez le marqueur au début de sa piste. Pour ce point de règle,
vous n'avez rien à faire, c'est le logiciel qui s'en occupe.

###############################################################################
"""

CONQUESTS = [
    (u'Domaine', 20, 5),
    (u'Duché', 30, 5),
    (u'Province', 30, 7),
    (u'Royaume', 40, 5),
    (u'Empire', 40, 7),
    ]

class DomiSolo(object):

    DEFAULT_EVENTS = [
        (u"Architecte", u"Achat d'un bâtiment : coût -1 pièce."),
        (u"Banditisme", u"Dévoilez les 2 premières cartes de votre deck. Si vous dévoilez une carte trésor, écartez là, si vous en révélez 2, écartez la plus élevée. Défaussez l'autre carte."),
        (u"Banque", u"Vous pouvez écarter des cartes Trésor de votre main contre des cartes Trésor pour la valeur (et non le prix) de la carte (Ag-2, Or-3)"),
        (u"Colporteur", u"+1 achat (pour +1 pièce)"),
        (u"Emeutes", u"Prenez une carte malédiction"),
        (u"Impôt Royal", u"-Phase d'achat- Vous ne pouvez dépenser que la moitié (arrondie à l'entier supérieur) de vos pièces disponibles (Trésor et Action)"),
        (u"Inquisition", u"-Phase action- Les cartes Sorcière, Laboratoire, Festin et Bibliothèque sont interdites / -Phase achat- Les cartes Chapelle, Milice, Chancelier et Bureaucrate coûtent -1 pièce"),
        (u"Invasion", u"Défaussez vous de cartes jusqu'à n'en avoir plus que 3 en main"),
        (u"Peste", u"-Phase d'action- Vous ne pouvez poser aucune carte Personnage"),
        (u"Saison Faste", u"+2 pièces"),
        (u"Sécheresse", u"Ne piochez que 3 cartes lors de la phase d'ajustement"),
        (u"Tremblement de terre", u"-Phase d'action- Vous ne pouvez poser aucune carte Bâtiment"),
        ]

    SEASONS = ['Printemps', 'été', 'automne', 'hiver']

    MAX_YEAR = 5

    def __init__(self, markers_cells, victory_target):
        self.events = self.shuffleArray(self.DEFAULT_EVENTS)
        self.year = 0
        self.season = 0
        self.current_turn = 0
        self.curse = 0
        self.army = 0
        self.treasure = 0
        self.max_army = markers_cells
        self.max_treasure = markers_cells
        self.victory_target = victory_target

    def shuffleArray(self, src_array):
        array_copy = src_array[:]
        dst_array = []
        while len(array_copy) > 0:
            dst_array.append(array_copy.pop(random.randrange(len(array_copy))))
        return dst_array

    def gameTurn(self):
        event_name, event_desc = self.events.pop()
        print u"Tour", self.current_turn, u"(", self.SEASONS[self.season], u"année", self.year,u") Marqueurs : Armée", self.army,u"- Tresor",self.treasure,u"/ Objectif",self.victory_target - self.curse
        print event_name,":",event_desc
        #print "Vous pouvez effeectuer votre action et votre achat, en respectant les consignes ci-dessus. Defaussez ensuite toutes les cartes et reconstituez-vous une main de 5 cartes"
        print u"[a: marqueur armée (Milice ou Espion)/t: marqueur trésor (Voleur ou Bureaucrate)/m: malédiction (Sorcière)/q: quitter/Entrée: fin du tour]"
        answer = None
        while answer is None or answer in ('a','t','m'):
            answer = raw_input()
            if answer == "a":
                self.army += 1
                if self.army == self.max_army:
                    self.curse += 1
                    self.army = 0
            elif answer == "t":
                self.treasure += 1
                if self.treasure == self.max_treasure:
                    self.curse += 1
                    self.treasure = 0
            elif answer == "m":
                self.curse += 1
        if answer == 'q':
            self.running = False
        self.season += 1
        if self.season >= len(self.SEASONS):
            self.season = 0
            self.year += 1
            if self.year == self.MAX_YEAR:
                print u"Jeu terminé... Objectif a atteindre : ", self.victory_target - self.curse
                self.running = False
            elif self.year % 2 == 0:
                print u"On mélange les évènements"
                self.events = self.shuffleArray(self.DEFAULT_EVENTS)
        print u"Le temps passe..."
        print
        print

    def run(self):
        self.running = True
        while self.running:
            self.gameTurn()
            self.current_turn += 1

class TextUI(object):

    def chooseConquest(self):
        answer = None
        while answer not in ('1','2','3','4','5','q'):
            print u"""Choisissez votre conquête (difficulté):
    %s

    q - Quitter
    """ % ("""
    """.join([u"%d - %s - %d points - %d cases""" % (i+1, c[0], c[1], c[2]) for i, c in enumerate(CONQUESTS)]),)
            answer = raw_input()
        if answer == 'q':
            return None
        answer = int(answer) - 1
        return CONQUESTS[answer][1], CONQUESTS[answer][2]

    def usage(self):
        print USAGE

def main():
    ui = TextUI()
    ui.usage()
    quest = ui.chooseConquest()
    if quest is not None:
        points, cells = quest
        ds = DomiSolo(cells, points)
        ds.run()

if __name__ == "__main__":
    main()

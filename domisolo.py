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
solitaire. Cette variante a ete creee par Bastien Nemett et est disponible ici:
http://www.trictrac.net/jeux/forum/viewtopic.php?p=1334034

Le but du jeu est d'obtenir, en 20 tours de jeu, plus de point q'une province
choisie en debut de partie (les cartes "Conquete")

Selectionnez de la facon qui vous plaira les 10 cartes royaumes avec lesquelles
vous jouerez.

Au debut de chaque tour de jeu, un evenement vous sera presente. Celui-ci
influencera vos differentes phases du jeu.

A la fin de chaque tour de jeu, le temps passe. Vous avez 20 tours avant la fin
de la partie.

Quelques ajustement des cartes Action/Attaque et Action/Reaction
================================================================

Sorciere : Piochez 2 cartes + Posez une carte malediction sur la carte
"Conquete" que vous avez choisie

Milice : +2 pieces / Avancez le marqueur "Armee" d'une case sur la carte
conquete

Voleur : Prenez 1 cuivre / Avancez le marqueur "Tresor" d'une case sur la carte
conquete

Espion : Regardez la carte du sommet de votre deck. Choisissez si vous la
defaussez ou non + Avancez le marqueur "Armee" d'une case sur la carte conquete

Bureaucrate : Recevez 1 argent / Avancez le marqueur "Tresor" d'une case sur la
carte conquete

A chaque fois q'un marqueur "Armee" ou "Tresor" atteint la derniere case de sa
piste sur la carte "conquete", posez une carte malediction sur la carte
conquete et remettez le marqueur au debut de sa piste. Pour ce point de regle,
vous n'avez rien a faire, c'est le logiciel qui s'en occupe.

###############################################################################
"""

CONQUESTS = [
    ('Domaine', 20, 5),
    ('Duche', 30, 5),
    ('Province', 30, 7),
    ('Royaume', 40, 5),
    ('Empire', 40, 7),
    ]

class DomiSolo(object):

    DEFAULT_EVENTS = [
        ("Architecte", "Achat d'un batiment : cout -1 piece."),
        ("Banditisme", "Devoilez les 2 premieres cartes de votre deck. Si vous devoilez une carte tresor, ecartez la, si vous en revelez 2, ecartez la plus elevee. Defaussez l'autre carte."),
        ("Banque", " Vous pouvez ecarter autant de cartes Tresors de votre que main que vous le souhaitez, recevez ensuite les cartes Tresors de votre choix d'une valeur totale inferieure ou egale au cout des cartes ecartees, ajouter ces cartes a votre main."),
        ("Colporteur", "+1 achat (pour +1 piece)"),
        ("Emeutes", "Prenez une carte malediction"),
        ("Impot Royal", "-Phase d'achat- Vous ne pouvez depenser que la moitie (arrondie a l'entier superieur) de vos pieces disponibles (Tresor et Action)"),
        ("Inquisition", "-Phase action- Les cartes Sorciere, Laboratoire, Festin et Bibliotheque sont interdites / -Phase achat- Les cartes Chapelle, Milice, Chancelier et Bureaucrate coutent -1 piece"),
        ("Invasion", "Defaussez vous de cartes jusq'a n'en avoir plus que 3 en main"),
        ("Peste", "-Phase d'action- Vous ne pouvez poser aucune carte Personnage"),
        ("Saison Faste", "+2 pieces"),
        ("Secheresse", "Ne piochez que 3 cartes lors de la phase d'ajustement"),
        ("Tremblement de terre", "-Phase d'action- Vous ne pouvez poser aucune carte Batiment"),
        ]

    SEASONS = ['Printemps', 'ete', 'automne', 'hiver']

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
        print "Tour", self.current_turn, "(", self.SEASONS[self.season], "annee", self.year,") Marqueurs : Armee", self.army,"- Tresor",self.treasure,"/ Objectif",self.victory_target - self.curse
        print event_name,":",event_desc
        #print "Vous pouvez effeectuer votre action et votre achat, en respectant les consignes ci-dessus. Defaussez ensuite toutes les cartes et reconstituez-vous une main de 5 cartes"
        answer = None
        while answer is None or answer in ('a','t','m','h'):
            print "[a: marqueur armee (Milice ou Espion)/t: marqueur tresor (Voleur ou Bureaucrate)/m: malediction (Sorciere)/q: quitter/Entree: fin du tour/h: help]"
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
            elif answer == "h":
                print USAGE
        if answer == 'q':
            self.running = False
        self.season += 1
        if self.season >= len(self.SEASONS):
            self.season = 0
            self.year += 1
            if self.year == self.MAX_YEAR:
                print "Jeu termine... Objectif a atteindre : ", self.victory_target - self.curse
                self.running = False
            elif self.year % 2 == 0:
                print "On melange les evenements"
                self.events = self.shuffleArray(self.DEFAULT_EVENTS)
        print "Le temps passe..."
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
            print """Choisissez votre conquete (difficulte):
    %s

    q - Quitter
    """ % ("""
    """.join(["%d - %s - %d points - %d cases""" % (i+1, c[0], c[1], c[2]) for i, c in enumerate(CONQUESTS)]),)
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class DomiSolo(object):

    DEFAULT_EVENTS = [
        (u'Architecte', u"Achat d'un batiment, cout -1 piece"),
        (u'Banditisme', u"Devoilez les 2 premieres cartes de votre deck. Si vous devoilez une carte tresor, ecarrtez la, si vous en revelez 2, ecartez la plus elevee et defaussez l'autre carte"),
        (u'Banque', 'Vous pouvez érter des cartes Trér de votre main contre des cartes Trér pour la valeur (et non le prix) de la carte (Ag-2, Or-3) '),
        (u'Colporteur', '+1 achat (pour +1 piè) '),
        (u'Emeutes', 'Prenez une carte malediction'),
        (u' Impot royal', u"Phase d'achat- Vous ne pouvez dénser que la moitiéarrondie à'entier supéeur) de vos piès disponibles (Trér et Action)"),
        (u'Inquisition', '-Phase action- Les cartes Sorciè, Laboratoire, Festin et Bibliothèe sont interdites / -Phase achat- Les cartes Chapelle, Milice, Chancelier et Bureaucrate coû -1 piè'),
        (u'Invasion', u"Déussez vous de cartes jusqu'à'en avoir plus que 3 en main"),
        (u'Peste', u"-Phase d'action- Vous ne pouvez poser aucune carte Personnage"),
        (u'Saison Faste', '+2 piès'),
        (u'Secheresse', u"Ne piochez que 3 cartes lors de la phase d'ajustement"),
        (u'Tremblement de terre', u"-Phase d'action- Vous ne pouvez poser aucune carte Bâment"),
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
        print "[a: marqueur armee/t: marqueur tresor/m: malediction]"
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

def main():
    ds = DomiSolo(5,20)
    ds.run()

if __name__ == "__main__":
    main()

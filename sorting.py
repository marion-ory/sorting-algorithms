import math


# __________________________________________________________________________________#
#                         [            TRI BULLE        ]
# _________________________________________________________________________________#
class TriBulle:
    def __init__(self, donnees):
        self.liste = donnees.copy()
        self.nom = "Tri Bulle"

    def trier(self):
        permutation = True
        passage = 0
        while permutation == True:
            permutation = False
            passage = passage + 1
            for i in range(0, len(self.liste) - passage):
                if self.liste[i] > self.liste[i + 1]:
                    permutation = True
                    self.liste[i], self.liste[i + 1] = (
                        self.liste[i + 1],
                        self.liste[i],
                    )

        return self.liste


# ____________________________________________________________________________________#
#                         [            TRI SELECTION        ]
# ____________________________________________________________________________________#


class TriSelection:
    def __init__(self, donnees):
        self.liste = donnees.copy()
        self.nom = "Tri selection"

    def trier(self):
        n = len(self.liste)
        for i in range(0, n):
            index_min = i
            for j in range(i + 1, n):
                if self.liste[j] < self.liste[index_min]:
                    index_min = j

            if index_min != i:
                self.liste[i], self.liste[index_min] = (
                    self.liste[index_min],
                    self.liste[i],
                )

        return self.liste


# ____________________________________________________________________________________#
#                         [            TRI FUSION        ]
# ____________________________________________________________________________________#


class TriFusion:
    def __init__(self, donnees):
        self.nom = " Tri Fusion"
        self.liste = donnees.copy()

    def fusion(self, gauche, droite):
        resultat = []
        index_droite, index_gauche = 0, 0

        while index_gauche < len(gauche) and index_droite < len(droite):

            if gauche[index_gauche] <= droite[index_droite]:
                resultat.append(gauche[index_gauche])
                index_gauche += 1
            else:
                resultat.append(droite[index_droite])
                index_droite += 1

        resultat.extend(gauche[index_gauche:])
        resultat.extend(droite[index_droite:])
        return resultat

    def separer(self, liste):
        if len(liste) <= 1:
            return liste
        milieu = len(liste) // 2
        gauche = self.separer(liste[:milieu])
        droite = self.separer(liste[milieu:])

        return self.fusion(gauche, droite)

    def trier(self):
        self.liste = self.separer(self.liste)
        return self.liste


# ____________________________________________________________________________________#
#                         [            TRI PEIGNE        ]
# ____________________________________________________________________________________#
class TriPeigne:
    def __init__(self, donnees):
        self.liste = donnees.copy()
        self.nom = "Tri à peigne"

    def trier(self):
        permutation = True
        gap = len(self.liste)

        while (permutation == True) and (gap > 1):
            permutation = False
            gap = math.floor(gap / 1.3)
            if gap < 1:
                gap = 1
            for i in range(0, len(self.liste) - gap):

                if self.liste[i] > self.liste[i + gap]:
                    permutation = True
                    self.liste[i], self.liste[i + gap] = (
                        self.liste[i + gap],
                        self.liste[i],
                    )
        return self.liste


# ____________________________________________________________________________________#
#                         [            TRI RAPIDE       ]
# ____________________________________________________________________________________#

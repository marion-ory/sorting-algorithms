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
class TriRapide:
    def __init__(self, donnees):
        self.liste = donnees.copy()
        self.nom = "Tri Rapide"

#partitionnement
    def partition(self, debut, fin):
        pivot = self.liste[fin]
        i = debut
        j = debut

        while j < fin:
            if self.liste[j] <= pivot:
                self.liste[i], self.liste[j] = self.liste[j], self.liste[i]
                i += 1
            j += 1

        self.liste[fin], self.liste[i] = self.liste[i], self.liste[fin]
        return i   


#recursion
    def tri_rapide(self, debut, fin):
        if debut < fin:
            i = self.partition(debut, fin)
            self.tri_rapide(debut, i-1)
            self.tri_rapide(i+1, fin)

#demarrage
    def trier(self):
        self.tri_rapide(0, len(self.liste)-1)


# ____________________________________________________________________________________#
#                         [            TRI INSERTION       ]
# ____________________________________________________________________________________#
class TriInsertion:
    def __init__(self, donnees):
        self.liste = donnees.copy()
        self.nom = "Tri par Insertion"

    def trier(self):
        #taille liste
        N = len(self.liste)

#tant qu'on n'est pas sorti du tableau (j >= 0)
#ET que l'élément à gauche est plus grand que la clé
#on décale cet élément d'une case vers la droite
        for n in range(1, N):#on parcourt la liste depuis le 2eme element 
            cle = self.liste[n]
            j = n - 1#j demarre avant la cle

            while j >= 0 and self.liste[j] > cle :
                self.liste[j + 1] = self.liste[j]
                j = j - 1#recule d une position pour continuer la comparaison

            self.liste[j + 1] = cle # la boucle s'est arrêtée : on a trouvé la bonne place



# ____________________________________________________________________________________#
#                         [            TRI PAR TAS       ]
# ____________________________________________________________________________________#
class TriTas :
    def __init__(self, donnees):
        #copie pour ne pas utiliser l'original
        self.liste = donnees.copy()
        self.nom = "Tri par Tas"


    def tri_tas(self, n, i):
        #L = liste , #n = taille du tas , #i = indice    
            plus_grand = i #pere donc plus grand
            gauche = 2 *i+1 #indice fils de gauche
            droit = 2*i+2 #indice fils de droite


            #fils gauche existe et plus grand ?
            if gauche < n and self.liste[gauche] > self.liste[plus_grand]:
                 plus_grand = gauche

            #fils droit existe et plus grand ?
            if droit < n and self.liste[droit] > self.liste[plus_grand]:
                 plus_grand = droit 


            #si le plus grand n'est pas i on echange et on descend
            if plus_grand != i:
                 self.liste[i], self.liste[plus_grand] = self.liste[plus_grand], self.liste[i]
                 self.entasser(n, plus_grand)

    def trier(self):
        N = len(self.liste)
        #construction du tas
        for i in range (N//2-1, -1, -1): 
              self.entasser(N, i)

        #rangement dans l'ordre
        for i in range(N-1, 0, -1):
             self.liste[0], self.liste[i] = self.liste[i], self.liste[0]
             self.entasser(i, 0)
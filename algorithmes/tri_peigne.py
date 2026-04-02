import math  # floor arrondi un nombre à l'entier inférieur le plus proche


class TriPeigne:
    def __init__(self, donnees):
        self.liste = donnees.copy()
        self.nom = "Tri à peigne"

    def trier(self):
        permutation = True
        gap = len(self.liste)

        # on boucle tant que l'ecart est grand et qu'on fait un echange

        while (permutation == True) and (
            gap > 1
        ):  # dès que gap==1 algo finit par tribulle
            permutation = False  # je pars du principe que la liste triees est fausse
            gap = math.floor(gap / 1.3)  # on reduit l'ecart avec le facteur 1.3
            if gap < 1:
                gap = 1  # gap minimum de 1 pour comparer des données voisines
            for i in range(0, len(self.liste) - gap):  # pour ne pas sortir de la liste

                if (
                    self.liste[i] > self.liste[i + gap]
                ):  # on compare la 1ère et dernière clés
                    permutation = (
                        True  # je trouve des donnees à permutter donc je les échanges
                    )
                    self.liste[i], self.liste[i + gap] = (
                        self.liste[i + gap],
                        self.liste[i],
                    )  # on change les positions : A ,B = B, A
        return self.liste


# on etablit la classe avec self et les donnnees qu on va trier
# je crée un copy des données sinon mais futurs algo à testé seront erronés
# en suite je passe au tri à peigne
# pour ça j active la permutation les element de ma liste vont pouvoir passé d un coté de l autre
# j établi que mon gap est egal à la longueur de ma liste pour commencer avant de reduire à 1.3
# Je boucle tant que l ecart est grand et que je fait des echanges et tant que mon gap est superieur à 1
# et que mon gap = a mon gap arrondi /1.3
# je continu de comparer tant que mon gap n est pas à 1
# pour i dans la longueur de ma liste moins mon ecart
# si i dans ma liste  et i+ecart = i+ecart et i de ma liste la j inverse les positions
# et enfin je retourne ma liste

class TriFusion:
    def __init__(self, donnees):
        self.nom = " Tri Fusion"
        self.liste = donnees.copy()

    def fusion(self, gauche, droite):
        resultat = []  # j accueil les resultats
        index_droite, index_gauche = 0, 0  # je divise en deux parties

        while index_gauche < len(gauche) and index_droite < len(droite):
            # si plus petit d un coté ou de l autre j ajoute d un cote ou de l autre
            if gauche[index_gauche] <= droite[index_droite]:
                resultat.append(gauche[index_gauche])  # ajoute au resultat à gauche
                index_gauche += 1
            else:
                resultat.append(droite[index_droite])  # ajoute au resultat droite
                index_droite += 1

        resultat.extend(
            gauche[index_gauche:]
        )  # permet d ajouter une liste à la fin d une autre
        resultat.extend(droite[index_droite:])
        return resultat

    def separer(self, liste):
        if len(liste) <= 1:
            return liste
        milieu = len(liste) // 2
        gauche = self.separer(liste[:milieu])  # recursivité on divise la liste
        droite = self.separer(liste[milieu:])  # : =slicing

        return self.fusion(gauche, droite)

    def trier(self):
        self.liste = self.separer(self.liste)
        return self.liste


# methode de fusion
# je fais une variable vide pour accueillir le resultat
# je divise ma liste et suppose les premieres places de chaque coté de ma liste
# si l index gauche et plus petit que le droit
# alors j ajoute ce resultat à gauche
# pareil pour la droite
# si c est à gauche ajoute index gauche à la liste  pareil à droite

# methode separer
# je determine le milieu de la liste
# puis le milieu de la geuche et celui de droite pour creer des mini liste dans lequel je tri d un cote de l autre puis je fusionne

# methode trier je dis que ma liste elle est egal a ma liste fusionner separer puis trier?

class TriBulle:
    def __init__(self, donnees):
        self.liste = donnees.copy()
        self.nom = "Tri Bulle"

    def trier(self):
        permutation = True
        passage = 0
        while permutation == True:  # je force le premier tour
            permutation = False  # je pars du principe que la liste est en desordre tant que la permutation n a pas prouvé le contraire
            passage = (
                passage + 1
            )  # a chaque tour complet la bulle est à sa place definitive
            for i in range(
                0, len(self.liste) - passage
            ):  # on reduit la zone à chaque passage
                if self.liste[i] > self.liste[i + 1]:  # on compare les voisins
                    permutation = True
                    self.liste[i], self.liste[i + 1] = (
                        self.liste[i + 1],
                        self.liste[i],
                    )  # on switch

        return self.liste


# Le tri à bulle on compare deux valeurs voisine et on les switch
# je pars du principe que ma loiste à trier est fausse
# pour trier dans ma liste je la parcours et je fais un passage à chaque tour
# des que je trouve des valeurs à permutter je les switch par ordre croissant ou decroissant par ex
# je ne suis pas sur d avoir bien compris toute les lignes de codes

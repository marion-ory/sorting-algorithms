class TriInsertion:
    def __init__(self, donnees):
        self.liste = donnees.copy()
        self.nom = "Tri par Insertion"

    def trier(self):
        # taille liste
        N = len(self.liste)

        # tant qu'on n'est pas sorti du tableau (j >= 0)
        # ET que l'élément à gauche est plus grand que la clé
        # on décale cet élément d'une case vers la droite
        for n in range(1, N):  # on parcourt la liste depuis le 2eme element
            cle = self.liste[n]
            j = n - 1  # j demarre avant la cle

            while j >= 0 and self.liste[j] > cle:
                self.liste[j + 1] = self.liste[j]
                j = j - 1  # recule d une position pour continuer la comparaison

            self.liste[j + 1] = (
                cle  # la boucle s'est arrêtée : on a trouvé la bonne place
            )

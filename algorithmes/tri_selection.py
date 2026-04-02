class TriSelection:
    def __init__(self, donnees):
        self.liste = donnees.copy()
        self.nom = "Tri selection"

    def trier(self):
        n = len(self.liste)
        for i in range(0, n):  # i = index ou on va placer le plus petit element
            index_min = i
            for j in range(
                i + 1, n
            ):  # je cherche dans la liste si il y a plus petit que i
                if self.liste[j] < self.liste[index_min]:
                    index_min = j  # trouvé ! nouvelle position

            if (
                index_min != i
            ):  # si le plus petit trouvé n est pas celui de depart alors j inverse
                self.liste[i], self.liste[index_min] = (
                    self.liste[index_min],
                    self.liste[i],
                )

        return self.liste


# j etablis ma classe selection
# Pour trier je parcours la longueur de la liste
# je suppose que le chiffre i est le plus petit de la liste je le place en 1er
# puis je parcours à nouveau la liste je prends le plus petit je le copmpare à l index
# si il est plus petit je switch sinon je continue
# pas besoin de boucle while c est n longueur de liste qui determine le nombre de tour

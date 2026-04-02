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
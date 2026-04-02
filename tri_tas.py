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
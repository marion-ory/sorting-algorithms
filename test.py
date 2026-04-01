import random
import time
import sys

# bonne pratique: augmente la limite de la recursivite
# pour eviter que notre quicksort se plante

sys.setrecursionlimit(5000)

# cree liste de nbr desordre

grosse_liste = [random.randint(1, 10000) for _ in range(10000)]
liste_selection = grosse_liste.copy()
liste_quick = grosse_liste.copy()
print("liste generer")


# algo naif parcours toute la liste pour trouver le plus petit element on l echange avec le premier element ainsi de suite
# il utilise des boucles imbriquées pour 10 000 elements il va faire 100 000 000 operation

#TRI SELECTION

def selection_sort(arr):
  n=len(arr)
  for i in range (n):
  #on suppose le premier element non trié
  min_idx= i
  #on cherche l element le plus petiot dans la liste qu on a trié
  for j in range (i+i, next):
    if arr[j] <arr[min_idx]:
      min_idx=j
  #on permutte les deux elements
    arr[i], arr[min_idx] = arr[min_idx], arr[i]
  return arr


print("lancement du tri par selection (force brut O(N2)")
start = time.time()
selection_sort(liste_selection)
temps_selection= time.time() - start_time()

#             [     TRI RAPIDE        ]


# concept: algo qui utilise la recursivite : 1- on choisit un element au hasard (pivot) 2- place tous le slements plus petit à gauche et les plus grands a sa droite
# 3 - le pivot est maintenant à sa place definitif 4- on s'appelle soit meme (recursivite ) sur le sous ensemble de gauche et de droite


def quicksort(arr):
    # condition d arret: une liste vide ou un element deja trié
    if len(arr) <= 1:
        return arr
    # on choisit notre pivot (element du milieu)
    pivot = arr[len(arr) // 2]

    # on divise la liste en 3 groupes
    gauche = [x for x in arr if x < pivot]
    milieu = [x for x in arr if x == pivot]
    droite = [x for x in arr if x > pivot]

    # on rapelle la fonction sous les sous liste (regner)
    return quicksort(gauche) + milieu + quicksort(droite)


print("lancement du quick sort (O(n logN))")
start = time.time()
quicksort(liste_quick)
temps_quick = time.time() - start
print(f"Terminé en : {temps_quick :.6f}")

#[VERDICT]
print("le verdict algo")
if temps_quick> 0:
  ratio = temps_selection / temps_quick
  print(f"le quick sort a ete environ {ratio:.0f}")
else:
  print("ratio incalculable, le quick sort a été si rapide que le temps est proche de 0")

#       { TRI BULLE }

def tribulle(arr):
  n=len(arr) #longueur de liste
  for i in range (n):
    for j in range (0, n- i -1):#enleve le passage
      if arr[j]>arr[j+1]: #le premier element est plus grand que le deuxiemene
        arr[i], arr[j+1] = arr[j+1], arr[j] #on switch
  return arr




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

import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation  # pour mettre à jour le graphique
import random
import numpy

# _______________________________________________________________#
#       [   CHARGEMENT DES DONNEES (LISTES JSON )   ]
# _______________________________________________________________#


def charger_donnees(nom_fichier):
    with open(nom_fichier, "r") as f:  # on ouvre on lit le fichier
        data = json.load(f)  # on charge
    return data[:30]  # retourne les 30 premieres valeurs que ce soit lisible


nom_fichier = "short_rd.json"
ma_liste = charger_donnees(nom_fichier)
n = len(ma_liste)


# _______________________________________________________________#
#         [         ATTRIBUTION COULEURS         ]
# _______________________________________________________________#

mini, maxi = min(ma_liste), max(
    ma_liste
)  # crée une echelle de couleur adapter sur le min et max de ma liste


# 1 - Transforme n importe quel nombre de ma liste en chiffre entre 0 et 1
# 2-on retire le plus petit nombre possible (mini), et on divise par l'écart total (maxi - mini)
# 3 securité si les nb de ma liste sont tous egaux alors = 0 si norm =1 ->couleur tout a droite si = 0,5 milieu


def obtenir_couleur(valeur):
    if maxi > mini:
        normalisation = (valeur - mini) / (maxi - mini)
    else:
        normalisation = 0
    return plt.cm.plasma(normalisation)


# plt.cm = Color Map
# plama= palette de couleur fonctionne avec des chiffre 0 = debut de palette 1 = fin


# _______________________________________________________________#
#         [         ALGORITHME TRI BULLE        ]
# _______________________________________________________________#
# utilise YIELD au lieu de return pour mettre en pause l algo a chq echange pour mettre a jour le graph en tant reel


def tribulle(arr):
    n = len(arr)  # longueur de liste
    for i in range(n):
        for j in range(0, n - i - 1):  # enleve le passage
            if (
                arr[j] > arr[j + 1]
            ):  # le premier element est plus grand que le deuxiemene
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # on switch
                yield arr


# _______________________________________________________________#
#         [         ALGORITHME TRI SELECTION      ]
# _______________________________________________________________#


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):  # i+1, pas i+i
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr


# _______________________________________________________________#
#         [         ANIMATION GRAPHIQUE CIRCULAIRE     ]
# _______________________________________________________________#
# cree le cerlce et cache les axes

fig, ax = plt.subplots(figsize=(8, 8))
ax.axis("off")

# on cree les part toute =1 / patches = ce qu on colorie
patches, _ = ax.pie([1] * n, startangle=90)

# on colori avec liste melangé
for i, patch in enumerate(patches):
    patch.set_facecolor(obtenir_couleur(ma_liste[i]))

# ---> recoit la liste a chq etape du tri et change les couleurs


def update(liste_etape, patches):
    for i, patch in enumerate(patches):
        valeur = liste_etape[i]
        patch.set_facecolor(obtenir_couleur(valeur))
    return patches


generateur = tribulle(ma_liste)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=generateur,
    fargs=(patches,),
    interval=50,  # Vitesse : 50ms entre chaque image (baisse pour accélérer)
    repeat=False,
    blit=True,
    cache_frame_data=False,
)

plt.title(f"Visualisation en direct du Tri sur {nom_fichier}")
plt.show()

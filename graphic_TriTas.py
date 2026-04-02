import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation  # pour mettre à jour le graphique
import random
import numpy
import matplotlib.cm as cm  # AJOUTÉ pour la ColorMap
import matplotlib.colors as mcolors  # AJOUTÉ pour la Normalisation de la légende

# _______________________________________________________________#
#       [   CHARGEMENT DES DONNEES (LISTES JSON )   ]
# _______________________________________________________________#


def charger_donnees(nom_fichier):
    with open(nom_fichier, "r") as f:  # on ouvre on lit le fichier
        data = json.load(f)  # on charge
    return data[:30]  # retourne les 30 premieres valeurs que ce soit lisible


nom_fichier = "json_data/short_rd.json"
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
#         [         ALGORITHME TRI RAPIDE  ]
# _______________________________________________________________#
# utilise YIELD au lieu de return pour mettre en pause l algo a chq echange pour mettre a jour le graph en tant reel


def tri_tas_anime(arr):
    n = len(arr)
    # On travaille sur une copie pour l'animation
    liste_anim = list(arr)

    def entasser(n, i):
        plus_grand = i  # On initialise le plus grand comme la racine
        gauche = 2 * i + 1
        droite = 2 * i + 2

        # Si le fils gauche est plus grand que la racine
        if gauche < n and liste_anim[gauche] > liste_anim[plus_grand]:
            plus_grand = gauche

        # Si le fils droit est plus grand que le plus grand actuel
        if droite < n and liste_anim[droite] > liste_anim[plus_grand]:
            plus_grand = droite

        # Si le plus grand n'est pas la racine
        if plus_grand != i:
            liste_anim[i], liste_anim[plus_grand] = (
                liste_anim[plus_grand],
                liste_anim[i],
            )
            # ON YIELD : On voit l'élément descendre dans l'arbre
            yield list(liste_anim)

            # On continue d'entasser récursivement
            yield from entasser(n, plus_grand)

    # 1. Construire le tas (max heap)
    for i in range(n // 2 - 1, -1, -1):
        yield from entasser(n, i)

    # 2. Extraire les éléments un par un
    for i in range(n - 1, 0, -1):
        # On déplace la racine actuelle à la fin
        liste_anim[i], liste_anim[0] = liste_anim[0], liste_anim[i]
        # ON YIELD : On voit l'élément le plus grand se placer à la fin
        yield list(liste_anim)

        # On appelle entasser sur le tas réduit
        yield from entasser(i, 0)


# _______________________________________________________________#
#   DANS TON FICHIER graphic_TriTas.py, UTILISE :
# _______________________________________________________________#

generateur = tri_tas_anime(ma_liste)

# _______________________________________________________________#
#         [         ANIMATION GRAPHIQUE CIRCULAIRE     ]
# _______________________________________________________________#
# cree le cerlce et cache les axes

fig, ax = plt.subplots(figsize=(9, 8))  # Ajusté pour faire de la place à la légende
ax.axis("off")

# on cree les part toute =1 / patches = ce qu on colorie
patches, _ = ax.pie([1] * n, startangle=90)


# _______________________________________________________________#
#         [         AJOUT DE LA LÉGENDE COLORBAR     ]
# _______________________________________________________________#
# Création de l'objet de normalisation pour la légende
norm = mcolors.Normalize(vmin=mini, vmax=maxi)
# Création de la barre de couleur 'plasma' liée à la normalisation
sm = cm.ScalarMappable(cmap=plt.cm.plasma, norm=norm)
sm.set_array([])  # Nécessaire pour Matplotlib
# Positionnement de la Colorbar à droite du graphique
cbar = fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
# Label de l'axe de la légende pour expliquer le dégradé
cbar.set_label(
    "PetitNombre ← Échelle de Couleur → GrandNombre", rotation=270, labelpad=15
)


# on colori avec liste melangé
for i, patch in enumerate(patches):
    patch.set_facecolor(obtenir_couleur(ma_liste[i]))

# ---> recoit la liste a chq etape du tri et change les couleurs


def update(liste_etape, patches):
    for i, patch in enumerate(patches):
        valeur = liste_etape[i]
        patch.set_facecolor(obtenir_couleur(valeur))
    return patches


generateur = tri_tas_anime(ma_liste)  # generateur contient la liste etape par etape

ani = animation.FuncAnimation(
    fig,  # = fenetre
    update,  # change les part en couleur
    frames=generateur,  # chaque etape que le yield va nous donner
    fargs=(patches,),
    interval=100,  # Vitesse : 100ms pour que ce soit plus lisible avec la légende
    repeat=False,
    blit=True,  # optimisation change juste la couleur des part
    cache_frame_data=False,
)

plt.title(f"Visualisation en direct du Tri par Tas sur {nom_fichier}\n")
plt.show()

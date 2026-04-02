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
#         [         ALGORITHME TRI FUSION     ]
# _______________________________________________________________#
# utilise YIELD au lieu de return pour mettre en pause l algo a chq echange pour mettre a jour le graph en tant reel


def tri_fusion_anime(arr):
    # On travaille sur une copie globale pour que chaque étape soit visible sur toute la liste
    A = list(arr)
    n = len(A)

    def fusionner(gauche, droite, debut, fin):
        resultat = []
        i = j = 0

        while i < len(gauche) and j < len(droite):
            if gauche[i] <= droite[j]:
                resultat.append(gauche[i])
                i += 1
            else:
                resultat.append(droite[j])
                j += 1

        resultat.extend(gauche[i:])
        resultat.extend(droite[j:])

        # Mise à jour de la liste principale aux bonnes positions
        for k in range(len(resultat)):
            A[debut + k] = resultat[k]
            # On yield à chaque petit changement pour une animation fluide
            yield list(A)

    def separer(debut, fin):
        if fin - debut <= 1:
            return

        milieu = (debut + fin) // 2

        # On utilise "yield from" pour faire remonter les étapes des appels récursifs
        yield from separer(debut, milieu)
        yield from separer(milieu, fin)

        # On récupère les deux moitiés triées
        gauche = A[debut:milieu]
        droite = A[milieu:fin]

        yield from fusionner(gauche, droite, debut, fin)

    # Lancement de la récursion
    yield from separer(0, n)


# _______________________________________________________________#
#   DANS TON FICHIER graphic_TriFusion.py, UTILISE :
# _______________________________________________________________#

generateur = tri_fusion_anime(ma_liste)

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


generateur = tri_fusion_anime(ma_liste)  # generateur contient la liste etape par etape

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

plt.title(f"Visualisation en direct du Tri par Fusion sur {nom_fichier}\n")
plt.show()

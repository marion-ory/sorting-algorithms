import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# _______________________________________________________________#
#       [   CHARGEMENT DES DONNEES (LISTES JSON )   ]
# _______________________________________________________________#


def charger_donnees(nom_fichier):
    with open(nom_fichier, "r") as f:
        data = json.load(f)
    return data[:30]


nom_fichier = "json_data/short_rd.json"
ma_liste = charger_donnees(nom_fichier)
n = len(ma_liste)

# _______________________________________________________________#
#         [         ATTRIBUTION COULEURS         ]
# _______________________________________________________________#

mini, maxi = min(ma_liste), max(ma_liste)
COLOR_MAP = plt.cm.plasma


def obtenir_couleur(valeur):
    if maxi > mini:
        normalisation = (valeur - mini) / (maxi - mini)
    else:
        normalisation = 0
    return COLOR_MAP(normalisation)


# _______________________________________________________________#
#         [         ALGORITHME TRI SELECTION ANIME    ]
# _______________________________________________________________#


def tri_selection_anime(arr):
    n = len(arr)
    liste_anim = list(arr)

    for i in range(n):
        index_min = i
        # On scanne le reste de la liste
        for j in range(i + 1, n):
            if liste_anim[j] < liste_anim[index_min]:
                index_min = j

        # On échange le minimum trouvé avec l'élément à la position i
        if index_min != i:
            liste_anim[i], liste_anim[index_min] = liste_anim[index_min], liste_anim[i]

        # On yield après chaque placement définitif
        yield list(liste_anim)


# _______________________________________________________________#
#         [         STYLE DASHBOARD & ANIMATION     ]
# _______________________________________________________________#

# Configuration du style sombre pour la cohérence visuelle
plt.rcParams["text.color"] = "#58A6FF"
plt.rcParams["axes.labelcolor"] = "#8B949E"

fig, ax = plt.subplots(figsize=(10, 8), facecolor="#0D1117")
ax.set_facecolor("#0D1117")
ax.axis("off")

# Tracé circulaire avec séparateurs sombres (linewidth=1.5 pour le look technique)
patches, _ = ax.pie(
    [1] * n, startangle=90, wedgeprops={"edgecolor": "#0D1117", "linewidth": 1.5}
)

# --- COLORBAR STYLISÉE ---
norm = mcolors.Normalize(vmin=mini, vmax=maxi)
sm = cm.ScalarMappable(cmap=COLOR_MAP, norm=norm)
sm.set_array([])

cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.08)
cbar.outline.set_edgecolor("#30363D")
cbar.ax.yaxis.set_tick_params(color="#8B949E", labelcolor="#8B949E")
cbar.set_label(
    "VALEURS : MIN → MAX", color="#58A6FF", fontsize=10, fontweight="bold", labelpad=20
)

# Initialisation des couleurs avec la liste mélangée
for i, patch in enumerate(patches):
    patch.set_facecolor(obtenir_couleur(ma_liste[i]))


def update(liste_etape, patches):
    for i, patch in enumerate(patches):
        patch.set_facecolor(obtenir_couleur(liste_etape[i]))
    return patches


generateur = tri_selection_anime(ma_liste)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=generateur,
    fargs=(patches,),
    interval=150,  # Un peu plus lent pour bien voir le placement "un par un"
    repeat=False,
    blit=True,
    cache_frame_data=False,
)

plt.title(
    f"MONITORING FLUX : TRI PAR SÉLECTION",
    color="#58A6FF",
    fontsize=16,
    fontweight="bold",
    pad=20,
)

plt.tight_layout()
plt.show()

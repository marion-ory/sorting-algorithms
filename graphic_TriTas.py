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
    return data[:30]  # Garde 30 pour la lisibilité sur le cercle


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
#         [         ALGORITHME TRI TAS ANIME          ]
# _______________________________________________________________#


def tri_tas_anime(arr):
    n = len(arr)
    A = list(arr)

    def entasser(nb_entasser, k):
        """Maintient la propriété de tas max à l'index k dans un tas de taille nb_entasser."""
        max_idx = k
        gauche = 2 * k + 1
        droite = 2 * k + 2

        if gauche < nb_entasser and A[gauche] > A[max_idx]:
            max_idx = gauche
        if droite < nb_entasser and A[droite] > A[max_idx]:
            max_idx = droite

        if max_idx != k:
            A[k], A[max_idx] = A[max_idx], A[k]
            # ON YIELD : L'élément descend dans l'arbre visible sur le cercle
            yield list(A)
            # Récursion
            yield from entasser(nb_entasser, max_idx)

    # 1. Phase d'entassement (Build Max Heap)
    print("🧠 Construction du tas invisible...")
    for i in range(n // 2 - 1, -1, -1):
        yield from entasser(n, i)

    # 2. Phase d'extraction (Sort)
    print("🏆 Phase d'extraction et de placement final...")
    for i in range(n - 1, 0, -1):
        # On déplace la racine actuelle (le max) à la fin
        A[0], A[i] = A[i], A[0]
        # ON YIELD : Le max se place à sa position définitive
        yield list(A)
        # On refait le tas sur la partie réduite
        yield from entasser(i, 0)


# _______________________________________________________________#
#         [         STYLE DASHBOARD & ANIMATION     ]
# _______________________________________________________________#

# Setup du style sombre pour matcher l'AnalysePage
plt.rcParams["text.color"] = "#58A6FF"
plt.rcParams["axes.labelcolor"] = "#8B949E"

fig, ax = plt.subplots(figsize=(10, 8), facecolor="#0D1117")
ax.set_facecolor("#0D1117")
ax.axis("off")

# Création du Pie Chart avec les séparateurs sombres
# wedprops linewidth=1.5 donne un look néon/technique
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

# Initialisation des couleurs (liste mélangée)
for i, patch in enumerate(patches):
    patch.set_facecolor(obtenir_couleur(ma_liste[i]))


def update(liste_etape, patches):
    for i, patch in enumerate(patches):
        patch.set_facecolor(obtenir_couleur(liste_etape[i]))
    return patches


generateur = tri_tas_anime(ma_liste)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=generateur,
    fargs=(patches,),
    interval=100,  # Vitesse modérée car il y a beaucoup de micro-étapes
    repeat=False,
    blit=True,
    cache_frame_data=False,
)

plt.title(
    f"MONITORING FLUX : TRI PAR TAS (HEAP SORT)",
    color="#58A6FF",
    fontsize=16,
    fontweight="bold",
    pad=20,
)

plt.tight_layout()
plt.show()

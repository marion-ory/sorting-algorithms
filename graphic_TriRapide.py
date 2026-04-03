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
#         [         ALGORITHME TRI RAPIDE ANIME      ]
# _______________________________________________________________#


def tri_rapide_anime(arr):
    A = list(arr)

    def partitionner(debut, fin):
        pivot = A[fin]
        i = debut
        for j in range(debut, fin):
            if A[j] <= pivot:
                A[i], A[j] = A[j], A[i]
                i += 1
                yield list(A)  # On yield à chaque échange
        A[i], A[fin] = A[fin], A[i]
        yield list(A)
        return i

    def quicksort(debut, fin):
        if debut < fin:
            # On récupère le pivot tout en itérant sur les étapes de partition
            gen = partitionner(debut, fin)
            pivot_index = debut
            for etape in gen:
                yield etape
                # À la fin du générateur partitionner, l'état de la liste est mis à jour
                # On détermine l'index du pivot (i) pour la récursion

            # On retrouve l'index du pivot pour continuer la récursion
            # (Dans QuickSort, le pivot est l'élément qui a été placé à l'index i)
            # Pour l'animation, on ré-exécute la logique de partition sans yield pour trouver l'index
            i = debut
            temp_list = list(
                A
            )  # On travaille sur une copie locale pour trouver l'index
            pivot_val = temp_list[fin]
            idx = debut
            for k in range(debut, fin):
                if temp_list[k] <= pivot_val:
                    temp_list[idx], temp_list[k] = temp_list[k], temp_list[idx]
                    idx += 1

            yield from quicksort(debut, idx - 1)
            yield from quicksort(idx + 1, fin)

    yield from quicksort(0, len(A) - 1)


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

# Initialisation des couleurs
for i, patch in enumerate(patches):
    patch.set_facecolor(obtenir_couleur(ma_liste[i]))


def update(liste_etape, patches):
    for i, patch in enumerate(patches):
        patch.set_facecolor(obtenir_couleur(liste_etape[i]))
    return patches


generateur = tri_rapide_anime(ma_liste)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=generateur,
    fargs=(patches,),
    interval=80,  # Vitesse équilibrée pour bien voir le pivotement
    repeat=False,
    blit=True,
    cache_frame_data=False,
)

plt.title(
    f"MONITORING FLUX : TRI RAPIDE",
    color="#58A6FF",
    fontsize=16,
    fontweight="bold",
    pad=20,
)

plt.tight_layout()
plt.show()

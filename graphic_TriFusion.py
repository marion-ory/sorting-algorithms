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
    return data[:30]  # On reste sur 30 pour la clarté visuelle


nom_fichier = "json_data/short_rd.json"
ma_liste = charger_donnees(nom_fichier)
n = len(ma_liste)

# _______________________________________________________________#
#         [         ATTRIBUTION COULEURS         ]
# _______________________________________________________________#

mini, maxi = min(ma_liste), max(ma_liste)
COLOR_MAP = plt.cm.plasma  # Palette cohérente avec le reste du projet


def obtenir_couleur(valeur):
    if maxi > mini:
        normalisation = (valeur - mini) / (maxi - mini)
    else:
        normalisation = 0
    return COLOR_MAP(normalisation)


# _______________________________________________________________#
#         [         ALGORITHME TRI FUSION ANIME     ]
# _______________________________________________________________#


def tri_fusion_anime(arr):
    A = list(arr)
    n = len(A)

    def fusionner(debut, milieu, fin):
        gauche = A[debut:milieu]
        droite = A[milieu:fin]
        i = j = 0

        for k in range(debut, fin):
            if i < len(gauche) and (j >= len(droite) or gauche[i] <= droite[j]):
                A[k] = gauche[i]
                i += 1
            else:
                A[k] = droite[j]
                j += 1
            yield list(A)  # On capture l'état global à chaque insertion

    def separer(debut, fin):
        if fin - debut <= 1:
            return
        milieu = (debut + fin) // 2
        yield from separer(debut, milieu)
        yield from separer(milieu, fin)
        yield from fusionner(debut, milieu, fin)

    yield from separer(0, n)


# _______________________________________________________________#
#         [         STYLE DASHBOARD & ANIMATION     ]
# _______________________________________________________________#

# Configuration Dark Mode
plt.rcParams["text.color"] = "#58A6FF"
plt.rcParams["axes.labelcolor"] = "#8B949E"

fig, ax = plt.subplots(figsize=(10, 8), facecolor="#0D1117")
ax.set_facecolor("#0D1117")
ax.axis("off")

# Tracé initial du camembert avec séparateurs noirs
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


generateur = tri_fusion_anime(ma_liste)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=generateur,
    fargs=(patches,),
    interval=80,  # Le tri fusion a beaucoup d'étapes, 80ms est un bon compromis
    repeat=False,
    blit=True,
    cache_frame_data=False,
)

plt.title(
    f"MONITORING FLUX : TRI FUSION",
    color="#58A6FF",
    fontsize=16,
    fontweight="bold",
    pad=20,
)

plt.tight_layout()
plt.show()

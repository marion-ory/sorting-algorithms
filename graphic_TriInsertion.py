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
#         [         ALGORITHME TRI INSERTION      ]
# _______________________________________________________________#


def tri_insertion_anime(arr):
    N = len(arr)
    liste_anim = list(arr)
    for n_idx in range(1, N):
        cle = liste_anim[n_idx]
        j = n_idx - 1
        while j >= 0 and liste_anim[j] > cle:
            liste_anim[j + 1] = liste_anim[j]
            j = j - 1
            # On yield ici pour voir le "glissement" de l'élément
            yield list(liste_anim)
        liste_anim[j + 1] = cle
        yield list(liste_anim)


# _______________________________________________________________#
#         [         STYLE DASHBOARD DARK          ]
# _______________________________________________________________#

# Configuration des couleurs globales
plt.rcParams["text.color"] = "#58A6FF"
plt.rcParams["axes.labelcolor"] = "#8B949E"

# Création de la figure avec le fond GitHub Dark
fig, ax = plt.subplots(figsize=(10, 8), facecolor="#0D1117")
ax.set_facecolor("#0D1117")
ax.axis("off")

# Tracé circulaire avec bordures pour bien séparer les segments
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


# --- MISE À JOUR ---
def update(liste_etape, patches):
    for i, patch in enumerate(patches):
        patch.set_facecolor(obtenir_couleur(liste_etape[i]))
    return patches


generateur = tri_insertion_anime(ma_liste)

ani = animation.FuncAnimation(
    fig,
    update,
    frames=generateur,
    fargs=(patches,),
    interval=50,  # Un peu plus rapide pour fluidifier le décalage
    repeat=False,
    blit=True,
    cache_frame_data=False,
)

plt.title(
    f"MONITORING FLUX : TRI PAR INSERTION",
    color="#58A6FF",
    fontsize=16,
    fontweight="bold",
    pad=20,
)

plt.tight_layout()
plt.show()

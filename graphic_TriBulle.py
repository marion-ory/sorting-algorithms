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
    return data[:30]  # Garde 30 pour la lisibilité


nom_fichier = "json_data/short_rd.json"
ma_liste = charger_donnees(nom_fichier)
n = len(ma_liste)

# _______________________________________________________________#
#         [         ATTRIBUTION COULEURS         ]
# _______________________________________________________________#

mini, maxi = min(ma_liste), max(ma_liste)

# Utilisation de la Colormap 'magma' ou 'plasma' (très néon sur fond noir)
COLOR_MAP = plt.cm.plasma


def obtenir_couleur(valeur):
    if maxi > mini:
        normalisation = (valeur - mini) / (maxi - mini)
    else:
        normalisation = 0
    return COLOR_MAP(normalisation)


# _______________________________________________________________#
#         [         ALGORITHME TRI BULLE        ]
# _______________________________________________________________#


def tribulle(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield list(arr)  # On yield une copie pour éviter les bugs d'index


# _______________________________________________________________#
#         [         ANIMATION ET STYLE DASHBOARD     ]
# _______________________________________________________________#

# Configuration du style sombre global
plt.rcParams["text.color"] = "#58A6FF"  # Bleu clair dashboard
plt.rcParams["axes.labelcolor"] = "#8B949E"

fig, ax = plt.subplots(figsize=(10, 8), facecolor="#0D1117")  # Fond GitHub Dark
ax.set_facecolor("#0D1117")
ax.axis("off")

# Création du camembert (Pie Chart) avec des bordures fines pour séparer les éléments
# wedgeprops={'edgecolor': '#0D1117', 'linewidth': 1} crée l'effet de séparation propre
patches, _ = ax.pie(
    [1] * n, startangle=90, wedgeprops={"edgecolor": "#0D1117", "linewidth": 1.5}
)

# _______________________________________________________________#
#         [         COLORBAR STYLISÉE         ]
# _______________________________________________________________#

norm = mcolors.Normalize(vmin=mini, vmax=maxi)
sm = cm.ScalarMappable(cmap=COLOR_MAP, norm=norm)
sm.set_array([])

# On ajoute la barre de couleur
cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.08)
cbar.outline.set_edgecolor("#30363D")  # Bordure de la légende discrète
cbar.ax.yaxis.set_tick_params(color="#8B949E", labelcolor="#8B949E")  # Ticks grisés

cbar.set_label(
    "VALEURS : MIN → MAX", color="#58A6FF", fontsize=10, fontweight="bold", labelpad=20
)

# Initialisation des couleurs
for i, patch in enumerate(patches):
    patch.set_facecolor(obtenir_couleur(ma_liste[i]))


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
    interval=50,  # Plus rapide pour un effet "monitoring" dynamique
    repeat=False,
    blit=True,
    cache_frame_data=False,
)

plt.title(
    f"MONITORING FLUX : {nom_algo.upper() if 'nom_algo' in locals() else 'TRI BULLE'}",
    color="#58A6FF",
    fontsize=16,
    fontweight="bold",
    pad=20,
)

# Ajustement pour que rien ne soit coupé
plt.tight_layout()
plt.show()

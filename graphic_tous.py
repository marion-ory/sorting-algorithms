import matplotlib.pyplot as plt
import os
import sorting
import engine
import matplotlib as mpl  # Import pour gérer les paramètres globaux


class GraphicTous:
    def __init__(self, parent):
        self.runner = engine.BenchmarkRunner()
        # On définit le style néon avant de générer quoi que ce soit
        self.definir_style_neon()
        self.generer_dashboard_complet()

    def definir_style_neon(self):
        """Définit une charte graphique modern-dark néon."""
        # Couleur de fond : Un bleu-noir très profond
        bg_color = "#101626"
        # Couleur des grilles et textes secondaires : Un gris-bleu discret
        grid_color = "#3A4561"
        # Couleur du texte principal : Blanc pur
        text_color = "#FFFFFF"

        # Application des paramètres globaux de Matplotlib
        mpl.rcParams.update(
            {
                "figure.facecolor": bg_color,  # Fond de la fenêtre
                "axes.facecolor": bg_color,  # Fond de la zone de graphique
                "axes.edgecolor": grid_color,  # Couleur des axes
                "axes.labelcolor": text_color,  # Couleur des labels (s, n)
                "xtick.color": text_color,  # Couleur des graduations X
                "ytick.color": text_color,  # Couleur des graduations Y
                "grid.color": grid_color,  # Couleur de la grille
                "text.color": text_color,  # Couleur de tous les textes
                "font.family": "sans-serif",  # Police moderne
                "font.sans-serif": [
                    "Futura",
                    "Montserrat",
                    "Arial",
                ],  # Liste de polices préférées
            }
        )

    def generer_dashboard_complet(self):
        # ... (Configuration des tests identique à ton code précédent) ...
        tests = [
            {"n": 30, "path": "json_data/short_rd.json"},
            {"n": 100, "path": "json_data/medium_rd.json"},
            {"n": 5000, "path": "json_data/large_rd.json"},
            {"n": 6000, "path": "json_data/xlarge_rd.json"},
        ]

        algos = {
            "Bulle": sorting.TriBulle,
            "Insertion": sorting.TriInsertion,
            "Sélection": sorting.TriSelection,
            "Peigne": sorting.TriPeigne,
            "Fusion": sorting.TriFusion,
            "Rapide": sorting.TriRapide,
            "Tas": sorting.TriTas,
        }

        tailles_x = [t["n"] for t in tests]
        derniers_temps = []
        noms_algos = []

        # --- PALETTE NÉON pour les algos (cyan, magenta, vert-fluo...) ---
        palette_neon = [
            "#00FFFF",
            "#FF00FF",
            "#39FF14",
            "#FF4500",
            "#FFD700",
            "#9370DB",
            "#FF69B4",
        ]

        # Préparation de la figure (1 ligne, 3 colonnes)
        fig, (ax1, ax2, ax3) = plt.subplots(
            1, 3, figsize=(18, 7), facecolor=mpl.rcParams["figure.facecolor"]
        )

        # Titre Principal épuré
        fig.suptitle(
            "📊 ANALYSE COMPARATIVE DES ALGORITHMES DE TRI",
            fontsize=18,
            fontweight="light",
            fontname="Montserrat",
        )

        print("🚀 Génération du Dashboard néon...")

        # Compteur pour la palette néon
        idx_color = 0

        for nom, classe in algos.items():
            temps_y = []
            ram_y = []
            color_algo = palette_neon[idx_color % len(palette_neon)]

            for t in tests:
                if os.path.exists(t["path"]):
                    self.runner.lancer(classe, t["path"])
                    res = self.runner.resultats[-1]
                    temps_y.append(res["temps"])
                    ram_y.append(res["ram"])
                else:
                    temps_y.append(0)
                    ram_y.append(0)

            # --- Graphique 1 : TEMPS (Courbes) ---
            ax1.plot(
                tailles_x,
                temps_y,
                marker="o",
                color=color_algo,
                label=nom,
                linewidth=2,
                alpha=0.9,
            )

            # --- Graphique 2 : RAM (Courbes) ---
            ax2.plot(
                tailles_x,
                ram_y,
                marker="s",
                linestyle="--",
                color=color_algo,
                label=nom,
                linewidth=1.5,
                alpha=0.7,
            )

            # Pour le Bar Chart (dernier test)
            noms_algos.append(nom)
            derniers_temps.append(temps_y[-1])

            idx_color += 1

        # Configuration AXE 1 : TEMPS (Épuré)
        ax1.set_title("🕒 Temps = f(n)", fontsize=14, fontweight="light")
        ax1.set_yscale("log")
        ax1.set_ylabel("Secondes (Log Scale)")
        ax1.grid(
            True, which="both", linestyle=":", linewidth=0.5
        )  # Grille très discrète
        ax1.spines["top"].set_visible(False)  # On enlève les bordures du haut/droite
        ax1.spines["right"].set_visible(False)

        # Configuration AXE 2 : RAM (Épuré)
        ax2.set_title("🧠 RAM = f(n)", fontsize=14, fontweight="light")
        ax2.set_ylabel("Kilooctets (Ko)")
        ax2.grid(True, linestyle=":", linewidth=0.5)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)

        # Configuration AXE 3 : FOCUS FINAL (Bar Chart)
        ax3.bar(
            noms_algos,
            derniers_temps,
            color=palette_neon,
            edgecolor=mpl.rcParams["figure.facecolor"],
            alpha=0.8,
        )
        ax3.set_title("🏆 Vitesse sur 5000 éléments", fontsize=14, fontweight="light")
        ax3.set_ylabel("Temps (s)")
        ax3.tick_params(axis="x", rotation=45, labelsize=10)  # Typo plus petite sur X
        ax3.spines["top"].set_visible(False)
        ax3.spines["right"].set_visible(False)
        ax3.grid(axis="y", linestyle=":", linewidth=0.5)  # Grille seulement sur Y

        # Légende unique néon épurée en bas
        handles, labels = ax1.get_legend_handles_labels()
        leg = fig.legend(
            handles,
            labels,
            loc="lower center",
            ncol=len(algos),
            bbox_to_anchor=(0.5, 0.05),
            fontsize=10,
            frameon=False,
        )
        # On passe le texte de la légende en blanc
        for text in leg.get_texts():
            text.set_color(mpl.rcParams["text.color"])

        plt.tight_layout(rect=[0, 0.1, 1, 0.95])
        plt.show()

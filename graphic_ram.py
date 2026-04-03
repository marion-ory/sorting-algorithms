import matplotlib.pyplot as plt
import os
import sorting
import engine


class GraphRAM:
    def __init__(self, parent):
        self.runner = engine.BenchmarkRunner()
        self.generer_graphique_ram()

    def generer_graphique_ram(self):
        # 1. Config des fichiers
        tests = [
            {"n": 100, "path": "json_data/short_rd.json"},
            {"n": 500, "path": "json_data/medium_rd.json"},
            {"n": 2000, "path": "json_data/large_rd.json"},
            {"n": 5000, "path": "json_data/xlarge_rd.json"},
        ]

        # 2. Liste des algos avec des styles différents pour les distinguer
        # (nom, classe, style de ligne)
        algos_config = [
            ("Bulle (In-place)", sorting.TriBulle, "-"),  # Ligne pleine
            ("Insertion (In-place)", sorting.TriInsertion, "--"),  # Pointillés larges
            ("Sélection (In-place)", sorting.TriSelection, "-."),  # Point-tiret
            ("Peigne", sorting.TriPeigne, ":"),  # Petits points
            ("Fusion (Copy)", sorting.TriFusion, "-"),  # Ligne pleine (montera)
            ("Rapide", sorting.TriRapide, "--"),  # Pointillés
            ("Tas", sorting.TriTas, "-."),  # Point-tiret
        ]

        plt.figure(figsize=(12, 7))
        tailles_x = [t["n"] for t in tests]

        print("Analyse de la consommation RAM en cours...")

        for nom, classe, style in algos_config:
            ram_y = []
            for t in tests:
                if os.path.exists(t["path"]):
                    self.runner.lancer(classe, t["path"])
                    # On s'assure de bien récupérer la valeur RAM
                    res_ram = self.runner.resultats[-1].get("ram", 0)
                    ram_y.append(res_ram)
                else:
                    ram_y.append(0)

            # On utilise 'linestyle' pour essayer de voir les superpositions
            plt.plot(
                tailles_x,
                ram_y,
                marker="o",
                label=nom,
                linestyle=style,
                linewidth=2,
                alpha=0.8,
            )

        # --- MISE EN FORME ---
        plt.title(
            "Analyse de Complexité Spatiale : Mémoire = f(n)",
            fontsize=14,
            fontweight="bold",
        )
        plt.xlabel("Nombre d'éléments dans la liste (n)")
        plt.ylabel("Mémoire RAM additionnelle (Ko)")

        # ÉCHELLE LINÉAIRE : Indispensable pour comparer O(1) et O(n)
        plt.yscale("linear")

        plt.grid(True, which="both", linestyle="--", alpha=0.6)

        # On place la légende à l'extérieur si elle cache les données
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

        plt.tight_layout()
        plt.show()

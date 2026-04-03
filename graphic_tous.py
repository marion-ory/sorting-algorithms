import matplotlib.pyplot as plt
import os
import sorting
import engine


class GraphicTous:
    def __init__(self, parent):
        self.runner = engine.BenchmarkRunner()
        self.generer_graphique_lineaire()

    def generer_graphique_lineaire(self):
        # 1. Config des fichiers et tailles réelles
        tests = [
            {"n": 100, "path": "json_data/short_rd.json"},
            {"n": 500, "path": "json_data/medium_rd.json"},
            {"n": 2000, "path": "json_data/large_rd.json"},
            {"n": 5000, "path": "json_data/xlarge_rd.json"},
        ]

        # 2. Dictionnaire de tous les algos (sans doublons)
        algos = {
            "Bulle (n²)": sorting.TriBulle,
            "Insertion (n²)": sorting.TriInsertion,
            "Sélection (n²)": sorting.TriSelection,
            "Peigne": sorting.TriPeigne,
            "Fusion (n log n)": sorting.TriFusion,
            "Rapide (n log n)": sorting.TriRapide,
            "Tas (n log n)": sorting.TriTas,
        }

        plt.figure(figsize=(12, 7))
        tailles_x = [t["n"] for t in tests]

        print(" Calcul des courbes en cours... .")

        for nom, classe in algos.items():
            temps_y = []
            for t in tests:
                if os.path.exists(t["path"]):
                    self.runner.lancer(classe, t["path"])
                    temps_y.append(self.runner.resultats[-1]["temps"])
                else:
                    temps_y.append(0)

            plt.plot(tailles_x, temps_y, marker="o", label=nom, linewidth=2)

        # Style du graphique
        plt.title(
            "Comparaison des Algorithmes (Temps = f(n) )",
            fontsize=14,
            fontweight="bold",
        )
        plt.xlabel("Taille de la liste (n)")
        plt.ylabel("Temps d'exécution (secondes)")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()

        # Si le tri bulle est trop haut, décommente la ligne suivante pour l'échelle LOG
        # plt.yscale('log')

        plt.tight_layout()
        plt.yscale("log")  # Ajoute ceci pour voir les algos rapides !
        plt.show()

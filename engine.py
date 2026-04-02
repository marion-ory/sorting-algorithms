import tracemalloc
import time
import json
import math

# Import de tes classes depuis sorting.py
from sorting import (
    TriBulle,
    TriSelection,
    TriFusion,
    TriPeigne,
    TriRapide,
    TriInsertion,
    TriTas,
)


class ComplexityAnalyzer:
    """Analyse les écarts entre temps réel et complexité théorique."""

    COMPLEXITES = {
        "TriBulle": "O(n²)",
        "TriSelection": "O(n²)",
        "TriInsertion": "O(n²)",
        "TriFusion": "O(n log n)",
        "TriRapide": "O(n log n)",
        "TriPeigne": "O(n log n)",
        "TriTas": "O(n log n)",
    }

    def temps_theorique(self, nom_algo, temps_ref, n_ref, n_nouveau):
        complexite = self.COMPLEXITES.get(nom_algo, "O(n log n)")
        if complexite == "O(n²)":
            # Le temps scale au carré du ratio de taille
            ratio = (n_nouveau / n_ref) ** 2
        else:
            # Le temps scale selon n log n
            ratio = (n_nouveau * math.log2(n_nouveau)) / (n_ref * math.log2(n_ref))
        return round(temps_ref * ratio, 6)

    def comparer(self, nom_algo, temps_reel, temps_theorique):
        if not temps_theorique or temps_theorique == 0:
            return 0
        ecart = abs(temps_reel - temps_theorique) / temps_theorique * 100
        return round(ecart, 2)


class TimeAnalyzer:
    """Mesure le temps d'exécution sur une copie propre des données."""

    def mesurer(self, classe_algo, donnees):
        # On crée une copie NEUVE pour chaque essai (CRUCIAL pour éviter les 0)
        copie_travail = list(donnees)
        instance = classe_algo(copie_travail)

        debut = time.perf_counter()
        resultat = instance.trier()
        fin = time.perf_counter()

        return fin - debut, resultat


class MemoryAnalyzer:
    """Mesure le pic de consommation RAM."""

    def mesurer(self, classe_algo, donnees):
        tracemalloc.start()
        # Copie ici aussi pour ne pas impacter les autres mesures
        instance = classe_algo(list(donnees))
        instance.trier()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak / 1024  # Conversion en Ko


class BenchmarkRunner:
    """Cerveau du programme : gère les mesures et le stockage des résultats."""

    def __init__(self):
        self.chrono = TimeAnalyzer()
        self.ram = MemoryAnalyzer()
        self.complexity = ComplexityAnalyzer()
        self.temps_ref = {}  # Stocke (temps, n) de référence pour chaque algo
        self.resultats = []

    def lancer(self, classe_algo, nom_fichier):
        # Chargement des données depuis le JSON
        with open(nom_fichier, "r") as f:
            donnees_initiales = json.load(f)

        nom = classe_algo.__name__
        mesures = []
        liste_triee_finale = []

        # 3 répétitions pour obtenir une médiane précise
        for _ in range(3):
            duree, triee = self.chrono.mesurer(classe_algo, donnees_initiales)
            mesures.append(duree)
            liste_triee_finale = triee  # On capture la liste triée pour l'UI

        temps_final = sorted(mesures)[1]  # On prend la médiane
        consommation_ram = self.ram.mesurer(classe_algo, donnees_initiales)

        # Gestion de la complexité théorique
        n_actuel = len(donnees_initiales)
        theorique = None
        ecart = None

        # Si le fichier est un 'short', il sert de base de référence
        if "short" in nom_fichier:
            self.temps_ref[nom] = (temps_final, n_actuel)
        # Sinon, on calcule l'écart par rapport à la référence stockée
        elif nom in self.temps_ref:
            t_ref, n_ref = self.temps_ref[nom]
            theorique = self.complexity.temps_theorique(nom, t_ref, n_ref, n_actuel)
            ecart = self.complexity.comparer(nom, temps_final, theorique)

        # Stockage complet du résultat
        self.resultats.append(
            {
                "algo": nom,
                "fichier": nom_fichier,
                "temps": round(temps_final, 6),
                "ram": round(consommation_ram, 2),
                "complexite": self.complexity.COMPLEXITES.get(nom, "N/A"),
                "theorique": theorique,
                "ecart": ecart,
                "liste_finale": liste_triee_finale,  # <--- Utilisé par AnalysePage
            }
        )


class Reporter:
    """Affiche les résultats dans la console sous forme de tableau."""

    def afficher(self, resultats):
        print("\n" + "=" * 90)
        print(
            f"{'ALGORITHME':<15} {'FICHIER':<18} {'TEMPS (s)':<12} {'RAM (Ko)':<12} {'ÉCART %':<10}"
        )
        print("-" * 90)
        for r in resultats:
            ecart_str = f"{r['ecart']}%" if r["ecart"] is not None else "Ref (Short)"
            print(
                f"{r['algo']:<15} {r['fichier']:<18} {r['temps']:<12.6f} {r['ram']:<12.2f} {ecart_str:<10}"
            )
        print("=" * 90 + "\n")


if __name__ == "__main__":
    # Point d'entrée pour tester le moteur sans l'interface
    runner = BenchmarkRunner()
    reporter = Reporter()

    algos = [
        TriBulle,
        TriSelection,
        TriFusion,
        TriPeigne,
        TriRapide,
        TriInsertion,
        TriTas,
    ]
    fichiers = [
        "short_rd.json",
        "short_rv.json",
        "medium_rd.json",
        "medium_rv.json",
        "large_rd.json",
        "large_rv.json",
        "xlarge_rd.json",
        "xlarge_rv.json",
    ]

    for algo in algos:
        for f in fichiers:
            try:
                runner.lancer(algo, f)
            except FileNotFoundError:
                print(f"Fichier {f} non trouvé, passage au suivant...")

    reporter.afficher(runner.resultats)

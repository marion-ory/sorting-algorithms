import tracemalloc #mesure internes (on isole l'algo)
import time 
import json
import math
 
from sorting import (TriBulle, TriSelection, TriFusion,
                     TriPeigne, TriRapide, TriInsertion, TriTas)
 
 
class ComplexityAnalyzer:
 
    # complexités théoriques connues de chaque algo
    COMPLEXITES = {
        "TriBulle"     : "O(n²)",
        "TriSelection" : "O(n²)",
        "TriInsertion" : "O(n²)",
        "TriFusion"    : "O(n log n)",
        "TriRapide"    : "O(n log n)",
        "TriPeigne"    : "O(n log n)",
        "TriTas"       : "O(n log n)",
    }
 
    def temps_theorique(self, nom_algo, temps_ref, n_ref, n_nouveau):
        complexite = self.COMPLEXITES[nom_algo]
 
        if complexite == "O(n²)":
            # le temps scale au carré du ratio de taille
            ratio = (n_nouveau / n_ref) ** 2
 
        elif complexite == "O(n log n)":
            # le temps scale proportionnellement à n*log(n)
            ratio = (n_nouveau * math.log2(n_nouveau)) / (n_ref * math.log2(n_ref))
 
        return round(temps_ref * ratio, 6)
 
    def comparer(self, nom_algo, temps_reel, temps_theorique):
        # écart en % entre le temps réel et le temps théorique
        ecart = abs(temps_reel - temps_theorique) / temps_theorique * 100
        return round(ecart, 2)    
 
 
 
#lire fichier json
class DataLoader:
    def charger(self, nom_fichier):
        with open(nom_fichier, "r") as f:
            contenu = json.load(f)
 
        return contenu
    
 
#mesure temps
class TimeAnalyzer:
    def mesurer(self, classe_algo, donnees):
        instance = classe_algo(donnees)#instance de la classe
        debut = time.perf_counter()# compteur hardware
        instance.trier()#tri lancee
        fin = time.perf_counter()
        return fin - debut
    
 
#mesure RAM
class MemoryAnalyzer:
    def mesurer(self, classe_algo, donnees):
        tracemalloc.start()#demarre le tracker memoire
        #on instqncie et on trie
        instance = classe_algo(donnees)
        instance.trier()
#on récupère le pic mémoire atteint depuis le start()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak / 1024 #conversion en kilo-occtes pour une mesure precise
 
 
#benchmark
class BenchmarkRunner:
    def __init__(self):
        self.loader     = DataLoader()
        self.chrono     = TimeAnalyzer()        # FIX 1 : TimeAnalyser -> TimeAnalyzer
        self.ram        = MemoryAnalyzer()
        self.complexity = ComplexityAnalyzer()  # FIX 2 : ComplexityAnalyzer instancié
        self.temps_ref  = {}                    # FIX 3 : stocke le temps short par algo
        self.resultats  = []                    # stockage de tous les resultats 
 
    def lancer(self, classe_algo, nom_fichier):
        donnees = self.loader.charger(nom_fichier)
        #mesure du temps : mediane de 3 repetes pour un resultat correct
        mesure_temp = []
        for _ in range(3):
            mesure_temp.append(self.chrono.mesurer(classe_algo, donnees))
        temps = sorted(mesure_temp)[1]
 
        ram = self.ram.mesurer(classe_algo, donnees)
 
        # FIX 4 : calcul de complexite_theorique et ecart_pourcent
        nom        = classe_algo.__name__
        complexite = self.complexity.COMPLEXITES[nom]
        n_ref      = 1000             # taille de short
        n_nouveau  = len(donnees)     # taille du fichier actuel
        temps_ref  = self.temps_ref.get(nom)  # temps mesuré sur short pour cet algo
 
        if temps_ref is not None:
            theorique = self.complexity.temps_theorique(nom, temps_ref, n_ref, n_nouveau)
            ecart     = self.complexity.comparer(nom, temps, theorique)
        else:
            # pas encore de référence : on est sur short, on la stocke
            self.temps_ref[nom] = temps
            theorique = None
            ecart     = None
 
        self.resultats.append({
            "algo"       : nom,               # FIX 5 : "Algo" -> "algo" (cohérence avec Reporter)
            "fichier"    : nom_fichier,        # FIX 5 : "Fichier" -> "fichier"
            "temps"      : round(temps, 6),   # en secondes
            "ram"        : round(ram, 3),      # en Ko
            "complexite" : complexite,
            "theorique"  : theorique,
            "ecart"      : ecart,
        })
 
class Reporter:
    def afficher(self, resultats):
 
        # entête du tableau
        print("\n" + "=" * 75)
        print(f"{'ALGORITHME':<20} {'FICHIER':<20} {'TEMPS (s)':<15} {'RAM (Ko)':<10}")
        print("=" * 75)
 
        # une ligne par résultat
        for r in resultats:
            print(f"{r['algo']:<20} {r['fichier']:<20} {r['temps']:<15} {r['ram']:<10}")
 
        print("=" * 75 + "\n")    
 
 
if __name__ == "__main__":
    runner   = BenchmarkRunner()
    reporter = Reporter()
 
    algos = [TriBulle, TriSelection, TriFusion,
             TriPeigne, TriRapide, TriInsertion, TriTas]
 
    fichiers = ["short_rd.json", "medium_rd.json",
                "short_rv.json", "medium_rv.json"]
 
    for algo in algos:
        for fichier in fichiers:
            runner.lancer(algo, fichier)
 
    reporter.afficher(runner.resultats)
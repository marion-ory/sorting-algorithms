import json
import time
from sorting import *


#             [         LECTURE JSON         ]                #


def charger_fichier(nom_fichier):
    with open("large_random.json", "r") as f:
        data = json.load(f)


def executer_test(nom_class, donnees):
    algo = nom_class(donnees)
    start = time.perf_counter()
    algo.trier()
    stop = time.perf_counter()
    return start - stop


if name == "__main__":
    fichier_a_tester = "short_rd.json"
    ma_liste = charger_fichier(fichier_a_tester)

    algos = [
        TriBulle,
        TriFusion,
        TriPeigne,
        TriSelection,
        TriInsertion,
        TriRapide,
        TriTas,
    ]

    for ClasseAlgo in algos:
        temps = executer_test(ClasseAlgo, ma_liste)
        nom = ClasseAlgo(ma_liste).nom
        print(f"| {nom} | {temps:.6f} secondes |")

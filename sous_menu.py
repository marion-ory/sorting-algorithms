import customtkinter as ctk
import time
import random
import json
import os
import psutil  # Pour la RAM
from analysepage import AnalysePage

# Attention : vérifie que tes fonctions s'appellent bien TriBulle ou tribulle (la casse compte !)
from sorting import TriBulle, TriInsertion, TriFusion


class StableMenu(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Tris Stables - Configuration")
        self.geometry("500x650")  # Un peu plus haut pour le texte

        # S'assurer que la fenêtre passe devant
        self.attributes("-topmost", True)

        # --- TITRE ---
        self.label = ctk.CTkLabel(
            self, text="ALGORITHMES STABLES", font=("Arial", 20, "bold")
        )
        self.label.pack(pady=20)

        # --- BOUTONS INDIVIDUELS ---

        self.btn_bulle = ctk.CTkButton(
            self,
            text="Lancer Tri Bulle",
            # On passe : (parent=self, nom="Tri Bulle", fonction=TriBulle)
            command=lambda: AnalysePage(self, "Tri Bulle", TriBulle),
        )
        self.btn_bulle.pack(pady=10)

        self.btn_insertion = ctk.CTkButton(
            self,
            text="Lancer Tri Insertion",
            # On passe : (parent=self, nom="Tri par Insertion", fonction=TriInsertion)
            command=lambda: AnalysePage(self, "Tri par Insertion", TriInsertion),
        )
        self.btn_insertion.pack(pady=10)

        self.btn_fusion = ctk.CTkButton(
            self,
            text="Lancer Tri Fusion",
            # On passe : (parent=self, nom="Tri par Fusion", fonction=TriFusion)
            command=lambda: AnalysePage(self, "Tri par Fusion", TriFusion),
        )
        self.btn_fusion.pack(pady=10)

        # --- SECTION COMPARAISON ---
        self.separator = ctk.CTkFrame(self, height=2, fg_color="gray")
        self.separator.pack(fill="x", pady=20, padx=20)

        self.btn_compare = ctk.CTkButton(
            self,
            text=" COMPARER TOUS LES STABLES",
            fg_color="#2A9D8F",
            hover_color="#21867A",
            command=self.comparer_algos,
        )
        self.btn_compare.pack(pady=20)

        self.result_box = ctk.CTkTextbox(self, width=450, height=200)
        self.result_box.pack(pady=10)

    def comparer_algos(self):
        chemin_fichier = "json_data/short_rv.json"

        if not os.path.exists(chemin_fichier):
            self.result_box.delete("0.0", "end")
            self.result_box.insert("0.0", f"Erreur : {chemin_fichier} introuvable.")
            return

        with open(chemin_fichier, "r") as f:
            liste_originale = json.load(f)

        # TOUT LE CODE CI-DESSOUS DOIT ÊTRE ALIGNÉ ICI (DANS LA FONCTION)
        taille = len(liste_originale)
        resultats = f"📊 COMPARAISON (Fichier: {chemin_fichier} | Taille: {taille})\n"
        resultats += "-" * 55 + "\n"
        resultats += f"{'Algorithme':<15} | {'Temps (s)':<12} | {'RAM (MB)':<10}\n"
        resultats += "-" * 55 + "\n"

        # On utilise les noms exacts de tes imports depuis sorting.py
        algos = {"Bulle": TriBulle, "Insertion": TriInsertion, "Fusion": TriFusion}
        process = psutil.Process(os.getpid())

        for nom, fonction in algos.items():
            liste_a_trier = liste_originale.copy()

            mem_avant = process.memory_info().rss / 1024 / 1024
            start = time.time()

            fonction(liste_a_trier)  # Appel de la fonction

            end = time.time()
            mem_apres = process.memory_info().rss / 1024 / 1024
            conso_mem = mem_apres - mem_avant

            resultats += (
                f"{nom:<15} | {end - start:<12.5f} | {max(0, conso_mem):<10.2f}\n"
            )

        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", resultats)

    def lancer_un_tri(self, nom):
        # Ici tu pourras plus tard appeler la visualisation spécifique
        print(f"Lancement du {nom}...")

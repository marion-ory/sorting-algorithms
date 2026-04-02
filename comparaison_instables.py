import customtkinter as ctk
import os
import json
import engine  # Importation de ton fichier engine.py
import subprocess
import sys
import matplotlib.pyplot as plt
import sorting  # Import indispensable pour comparer les classes d'algo


class AnalysePage(ctk.CTkToplevel):
    def __init__(self, parent, nom_algo, classe_algo):
        super().__init__(parent)
        self.title(f"Analyse Performance - {nom_algo}")
        self.geometry("700x950")

        # On stocke l'algorithme (la CLASSE) et son nom
        self.classe_algo = classe_algo
        self.nom_algo = nom_algo

        # On instancie ton moteur de calcul
        self.runner = engine.BenchmarkRunner()

        # --- TITRE DYNAMIQUE ---
        self.label_titre = ctk.CTkLabel(
            self, text=f"ANALYSE : {nom_algo}", font=("Arial", 22, "bold")
        )
        self.label_titre.pack(pady=20)

        # --- ZONE CONFIGURATION ---
        self.frame_config = ctk.CTkFrame(self)
        self.frame_config.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.frame_config, text="Choisir le jeu de données :").pack(pady=5)

        # --- UTILISATION DE JSON_DATA ---
        self.options_listes = [
            "json_data/short_rd.json",
            "json_data/short_rv.json",
            "json_data/medium_rd.json",
            "json_data/medium_rv.json",
            "json_data/large_rd.json",
            "json_data/large_rv.json",
            "json_data/xlarge_rd.json",
            "json_data/xlarge_rv.json",
        ]

        self.combo_liste = ctk.CTkComboBox(
            self.frame_config, values=self.options_listes, width=300
        )
        self.combo_liste.pack(pady=10)
        self.combo_liste.set("json_data/short_rd.json")

        # --- BOUTONS D'ACTION ---
        self.frame_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_buttons.pack(pady=15)

        # 1. Bouton Benchmark
        self.btn_run = ctk.CTkButton(
            self.frame_buttons,
            text="ANALYSE COMPLEXITE",
            fg_color="#2A9D8F",
            width=140,
            height=40,
            font=("Arial", 13, "bold"),
            command=self.executer_mesures,
        )
        self.btn_run.pack(side="left", padx=5)

        # 2. Bouton Graphique (Animation)
        self.btn_graph = ctk.CTkButton(
            self.frame_buttons,
            text="GRAPHIQUE",
            fg_color="#E76F51",
            width=140,
            height=40,
            font=("Arial", 13, "bold"),
            command=self.ouvrir_graphique,
        )
        self.btn_graph.pack(side="left", padx=5)

        # --- RÉSULTATS STATS ---
        self.stats_box = ctk.CTkTextbox(
            self, width=540, height=150, font=("Courier", 13)
        )
        self.stats_box.pack(pady=10)

        # --- ZONE DE SYNTHÈSE ---
        self.frame_synthese = ctk.CTkFrame(
            self,
            fg_color="#F0F0F0",
            corner_radius=15,
            border_width=2,
            border_color="#2A9D8F",
        )
        self.frame_synthese.pack(pady=20, padx=20, fill="both", expand=True)

        self.text_synthese = ctk.CTkLabel(
            self.frame_synthese,
            text="En attente de calcul...",
            wraplength=480,
            font=("Consolas", 11),
            text_color="#333333",
            justify="left",
        )
        self.text_synthese.pack(pady=15, padx=20)

    def executer_mesures(self):
        nom_fichier = self.combo_liste.get()
        if not os.path.exists(nom_fichier):
            self.stats_box.insert("0.0", f"⚠️ Erreur : {nom_fichier} introuvable\n")
            return

        self.runner.lancer(self.classe_algo, nom_fichier)
        res = self.runner.resultats[-1]

        self.stats_box.delete("0.0", "end")
        self.stats_box.insert(
            "0.0",
            f"--- RÉSULTATS {self.nom_algo.upper()} ---\n"
            f"Fichier    : {nom_fichier}\n"
            f"Complexité : {res['complexite']}\n"
            f"Temps      : {res['temps']:.6f} sec\n"
            f"Mémoire    : {res['ram']:.2f} Ko",
        )

        # Aperçu avant/après
        with open(nom_fichier, "r") as f:
            data = json.load(f)

        texte_final = f"📥 AVANT : {data[:15]}...\n"
        texte_final += f"📤 APRÈS : {res.get('liste_finale', [])[:15]}...\n"
        texte_final += "─" * 45 + "\n"
        texte_final += self.generer_phrase_synthese(res, nom_fichier)
        self.text_synthese.configure(text=texte_final)

    def ouvrir_graphique(self):
        nom_script = f"graphic_{self.classe_algo.__name__}.py"
        if os.path.exists(nom_script):
            subprocess.Popen([sys.executable, nom_script])
        else:
            self.stats_box.insert("0.0", f"⚠️ Fichier {nom_script} manquant\n")

    def generer_phrase_synthese(self, res, fichier):
        """Génère un petit texte explicatif basé sur les résultats du benchmark."""
        # Détermine si c'est une liste aléatoire ou inversée
        type_liste = "aléatoire" if "_rd" in fichier else "inversée (pire cas)"

        # Petit commentaire sur la performance
        if res["temps"] < 0.01:
            vitesse = "foudroyante ⚡"
        elif res["temps"] < 0.1:
            vitesse = "très satisfaisante ✅"
        else:
            vitesse = "plus lente (logique pour cet algorithme) 🐢"

        phrase = f"💡 ANALYSE : Sur cette liste {type_liste}, la vitesse a été {vitesse}.\n\n"
        phrase += f"La complexité observée est de type {res['complexite']}.\n"

        # Si ton engine calcule l'écart théorique
        if res.get("ecart") is not None:
            phrase += f"L'écart avec la théorie est de {res['ecart']}%."

        return phrase

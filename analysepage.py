import customtkinter as ctk
import os
import json
import engine  # Importation de ton fichier engine.py
import subprocess
import sys


class AnalysePage(ctk.CTkToplevel):
    def __init__(self, parent, nom_algo, classe_algo):
        super().__init__(parent)
        self.title(f"Analyse Performance - {nom_algo}")
        self.geometry("600x900")  # Hauteur ajustée pour le nouveau bouton

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

        ctk.CTkLabel(self.frame_config, text="Choisir le jeu de données (JSON) :").pack(
            pady=5
        )

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
        self.frame_buttons.pack(pady=10)

        # Bouton Benchmark
        self.btn_run = ctk.CTkButton(
            self.frame_buttons,
            text="LANCER LE BENCHMARK",
            fg_color="#2A9D8F",
            height=40,
            font=("Arial", 14, "bold"),
            command=self.executer_mesures,
        )
        self.btn_run.pack(side="left", padx=10)

        # Bouton Graphique (Nouveau)
        self.btn_graph = ctk.CTkButton(
            self.frame_buttons,
            text="GRAPHIQUE ",
            fg_color="#E76F51",  # Couleur corail pour le différencier
            height=40,
            font=("Arial", 14, "bold"),
            command=self.ouvrir_graphique,
        )
        self.btn_graph.pack(side="left", padx=10)

        # --- RÉSULTATS STATS ---
        self.stats_box = ctk.CTkTextbox(
            self, width=500, height=150, font=("Courier", 13)
        )
        self.stats_box.pack(pady=10)

        # --- ZONE DE SYNTHÈSE ET APERÇU (LISIBLE) ---
        self.frame_synthese = ctk.CTkFrame(
            self,
            fg_color="#F0F0F0",
            corner_radius=15,
            border_width=2,
            border_color="#2A9D8F",
        )
        self.frame_synthese.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_synthese_titre = ctk.CTkLabel(
            self.frame_synthese,
            text="💡 SYNTHÈSE & VISUALISATION",
            font=("Arial", 14, "bold"),
            text_color="#2A9D8F",
        )
        self.label_synthese_titre.pack(pady=5)

        self.text_synthese = ctk.CTkLabel(
            self.frame_synthese,
            text="En attente de calcul...",
            wraplength=480,
            font=(("Consolas", 11) if os.name == "nt" else ("Menlo", 11)),
            text_color="#333333",
            justify="left",
        )
        self.text_synthese.pack(pady=15, padx=20)

    def executer_mesures(self):
        nom_fichier = self.combo_liste.get()

        if not os.path.exists(nom_fichier):
            return

        with open(nom_fichier, "r") as f:
            donnees_avant = json.load(f)
        apercu_avant = str(donnees_avant[:20]) + (
            "..." if len(donnees_avant) > 20 else ""
        )

        self.runner.lancer(self.classe_algo, nom_fichier)
        res = self.runner.resultats[-1]

        liste_triee_par_algo = res.get("liste_finale", [])
        apercu_apres = str(liste_triee_par_algo[:20]) + (
            "..." if len(liste_triee_par_algo) > 20 else ""
        )

        self.stats_box.delete("0.0", "end")
        self.stats_box.insert(
            "0.0",
            f"--- RÉSULTATS {self.nom_algo.upper()} ---\n"
            f"Fichier : {nom_fichier}\n"
            f"Complexité : {res['complexite']}\n"
            f"Temps Réel : {res['temps']:.6f} sec\n"
            f"Mémoire    : {res['ram']:.2f} Ko (Peak)",
        )

        texte_final = f"📥 AVANT (20 premiers) :\n{apercu_avant}\n\n"
        texte_final += f"📤 APRÈS (20 premiers) :\n{apercu_apres}\n"
        texte_final += "─" * 45 + "\n"
        texte_final += self.generer_phrase_synthese(res, nom_fichier)

        self.text_synthese.configure(text=texte_final)

    def ouvrir_graphique(self):
        """Lance le script graphique correspondant à l'algorithme actuel."""
        # On construit le nom : graphic_ + nom de la classe (ex: graphic_TriBulle.py)
        nom_script = f"graphic_{self.classe_algo.__name__}.py"

        if os.path.exists(nom_script):
            # subprocess.Popen lance le graphique sans bloquer l'interface principale
            subprocess.Popen([sys.executable, nom_script])
        else:
            self.stats_box.delete("0.0", "end")
            self.stats_box.insert(
                "0.0", f"⚠️ ERREUR : Fichier '{nom_script}' introuvable."
            )

    def generer_phrase_synthese(self, res, fichier):
        type_liste = "aléatoire" if "_rd" in fichier else "inversée (pire cas)"
        vitesse = "très efficace" if res["temps"] < 0.05 else "plus exigeant"

        phrase = f"Analyse : Sur cette liste {type_liste}, le tri a été {vitesse}.\n"

        if res.get("ecart") is not None:
            if res["ecart"] < 20:
                phrase += f"L'écart de {res['ecart']}% confirme la théorie {res['complexite']}."
            else:
                phrase += (
                    f"Écart théorique de {res['ecart']}% (lié à l'overhead Python)."
                )

        return phrase

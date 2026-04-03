import customtkinter as ctk
import os
import json
import engine
import subprocess
import sys
import sorting


class AnalysePage(ctk.CTkToplevel):
    def __init__(self, parent, nom_algo, classe_algo):
        super().__init__(parent)
        self.title(f"Terminal d'Analyse - {nom_algo}")
        self.geometry("700x900")
        self.configure(fg_color="#0D1117")

        # Force la fenêtre au premier plan
        self.attributes("-topmost", True)

        self.classe_algo = classe_algo
        self.nom_algo = nom_algo
        self.runner = engine.BenchmarkRunner()

        # --- 1. HEADER (Bandeau bleu du haut) ---
        self.header_frame = ctk.CTkFrame(
            self, fg_color="#161B22", height=80, corner_radius=0
        )
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        self.label_titre = ctk.CTkLabel(
            self.header_frame,
            text=f"📊 ENGINE MONITORING : {nom_algo.upper()}",
            font=("Arial", 20, "bold"),
            text_color="#58A6FF",
        )
        self.label_titre.pack(expand=True, fill="both")

        # --- 2. ZONE CONFIGURATION (Choix du fichier) ---
        self.frame_config = ctk.CTkFrame(
            self, fg_color="#161B22", border_width=1, border_color="#30363D"
        )
        self.frame_config.pack(pady=20, padx=30, fill="x")

        ctk.CTkLabel(
            self.frame_config,
            text="DATASET SOURCE",
            font=("Arial", 11, "bold"),
            text_color="#8B949E",
        ).pack(pady=(15, 0))

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
            self.frame_config,
            values=self.options_listes,
            width=400,
            fg_color="#0D1117",
            border_color="#30363D",
            button_color="#21262D",
        )
        self.combo_liste.pack(pady=20)
        self.combo_liste.set("json_data/short_rd.json")

        # --- 3. BOUTONS D'ACTION (Benchmark et Graphique) ---
        self.frame_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_buttons.pack(pady=10, fill="x")

        self.btn_run = ctk.CTkButton(
            self.frame_buttons,
            text="▶ EXECUTER LE BENCHMARK",
            fg_color="#238636",
            hover_color="#2EA043",
            width=220,
            height=45,
            font=("Arial", 13, "bold"),
            command=self.executer_mesures,
        )
        self.btn_run.pack(side="left", padx=(120, 10))  # Centrage manuel approximatif

        self.btn_graph = ctk.CTkButton(
            self.frame_buttons,
            text="📈 VOIR ANIMATION",
            fg_color="#1F6FEB",
            hover_color="#388BFD",
            width=220,
            height=45,
            font=("Arial", 13, "bold"),
            command=self.ouvrir_graphique,
        )
        self.btn_graph.pack(side="left", padx=10)

        # --- 4. STATS BOX (Console verte) ---
        self.stats_box = ctk.CTkTextbox(
            self,
            width=640,
            height=180,
            font=("Courier New", 14),
            fg_color="#010409",
            border_width=1,
            border_color="#30363D",
            text_color="#7EE787",
        )
        self.stats_box.pack(pady=20, padx=30)
        self.stats_box.insert("0.0", "> Système prêt. En attente d'instruction...")

        # --- 5. ZONE DE SYNTHÈSE (Rapport final) ---
        self.frame_synthese = ctk.CTkFrame(
            self,
            fg_color="#161B22",
            corner_radius=10,
            border_width=1,
            border_color="#58A6FF",
        )
        self.frame_synthese.pack(pady=(10, 30), padx=30, fill="both", expand=True)

        ctk.CTkLabel(
            self.frame_synthese,
            text="SYNTHÈSE DE L'ALGORITHME",
            font=("Arial", 12, "bold"),
            text_color="#58A6FF",
        ).pack(pady=(15, 0))

        self.text_synthese = ctk.CTkLabel(
            self.frame_synthese,
            text="Veuillez lancer l'analyse pour générer le rapport.",
            wraplength=550,
            font=("Arial", 13),
            text_color="#C9D1D9",
            justify="left",
        )
        self.text_synthese.pack(pady=20, padx=30)

    # --- MÉTHODES LOGIQUES (Ne pas oublier de les garder !) ---
    def executer_mesures(self):
        nom_fichier = self.combo_liste.get()
        if not os.path.exists(nom_fichier):
            self.stats_box.delete("0.0", "end")
            self.stats_box.insert(
                "0.0", f"❌ ERROR: Fichier {nom_fichier} introuvable\n"
            )
            return

        self.stats_box.delete("0.0", "end")
        self.stats_box.insert("0.0", f"🚀 Initialisation du tri sur {nom_fichier}...\n")

        self.runner.lancer(self.classe_algo, nom_fichier)
        res = self.runner.resultats[-1]

        self.stats_box.delete("0.0", "end")
        output = [
            f"🟢 BENCHMARK RÉUSSI",
            f"{'='*30}",
            f"ALGORITHME  : {self.nom_algo}",
            f"COMPLEXITÉ  : {res['complexite']}",
            f"TEMPS EXEC  : {res['temps']:.6f} s",
            f"USAGE RAM   : {res['ram']:.2f} Ko",
            f"{'='*30}",
        ]
        self.stats_box.insert("0.0", "\n".join(output))

        type_liste = "ALÉATOIRE (RD)" if "_rd" in nom_fichier else "INVERSÉE (RV)"
        synth = f"📋 RAPPORT D'ANALYSE\n\n"
        synth += f"L'algorithme a été testé sur une configuration {type_liste}.\n"
        synth += self.generer_phrase_synthese(res, nom_fichier)
        self.text_synthese.configure(text=synth)

    def ouvrir_graphique(self):
        nom_script = f"graphic_{self.classe_algo.__name__}.py"
        if os.path.exists(nom_script):
            subprocess.Popen([sys.executable, nom_script])
        else:
            self.stats_box.insert("end", f"\n⚠️ SCRIPT MANQUANT: {nom_script}")

    def generer_phrase_synthese(self, res, fichier):
        vitesse = "optimale (⚡)" if res["temps"] < 0.05 else "standard (✔)"
        return f"Conclusion : Performance {vitesse}.\nRAM : pic à {res['ram']:.2f} Ko."

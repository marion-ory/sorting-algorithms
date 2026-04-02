import customtkinter as ctk
import os
import json
import engine  # Importation de ton fichier engine.py


class AnalysePage(ctk.CTkToplevel):
    def __init__(self, parent, nom_algo, classe_algo):
        super().__init__(parent)
        self.title(f"Analyse Performance - {nom_algo}")
        self.geometry("600x850")  # Ajusté pour les listes de 20 éléments

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
            "short_rd.json",
            "short_rv.json",
            "medium_rd.json",
            "medium_rv.json",
            "large_rd.json",
            "large_rv.json",
            "xlarge_rd.json",
            "xlarge_rv.json",
        ]
        self.combo_liste = ctk.CTkComboBox(
            self.frame_config, values=self.options_listes, width=300
        )
        self.combo_liste.pack(pady=10)
        self.combo_liste.set("short_rd.json")

        # --- BOUTON CALCULER ---
        self.btn_run = ctk.CTkButton(
            self,
            text="🚀 LANCER LE BENCHMARK (ENGINE)",
            fg_color="#2A9D8F",
            height=40,
            font=("Arial", 14, "bold"),
            command=self.executer_mesures,
        )
        self.btn_run.pack(pady=20)

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
            font=(
                ("Consolas", 11) if os.name == "nt" else ("Menlo", 11)
            ),  # Taille légèrement réduite pour 20 éléments
            text_color="#333333",
            justify="left",
        )
        self.text_synthese.pack(pady=15, padx=20)

    def executer_mesures(self):
        nom_fichier = self.combo_liste.get()

        if not os.path.exists(nom_fichier):
            return

        # 1. Charger les données pour l'aperçu AVANT (20 éléments)
        with open(nom_fichier, "r") as f:
            donnees_avant = json.load(f)
        apercu_avant = str(donnees_avant[:20]) + (
            "..." if len(donnees_avant) > 20 else ""
        )

        # 2. Lancer le moteur (Engine)
        self.runner.lancer(self.classe_algo, nom_fichier)
        res = self.runner.resultats[-1]

        # 3. Récupérer l'APRÈS directement depuis le moteur (20 éléments)
        # On utilise le résultat réel de l'algorithme stocké dans le dictionnaire
        liste_triee_par_algo = res.get("liste_finale", [])
        apercu_apres = str(liste_triee_par_algo[:20]) + (
            "..." if len(liste_triee_par_algo) > 20 else ""
        )

        # 4. Affichage Stats
        self.stats_box.delete("0.0", "end")
        self.stats_box.insert(
            "0.0",
            f"--- RÉSULTATS {self.nom_algo.upper()} ---\n"
            f"Fichier : {nom_fichier}\n"
            f"Complexité : {res['complexite']}\n"
            f"Temps Réel : {res['temps']:.6f} sec\n"
            f"Mémoire    : {res['ram']:.2f} Ko (Peak)",
        )

        # 5. Affichage Visuel (Synthèse + Avant/Après)
        texte_final = f"📥 AVANT (20 premiers) :\n{apercu_avant}\n\n"
        texte_final += f"📤 APRÈS (20 premiers) :\n{apercu_apres}\n"
        texte_final += "─" * 45 + "\n"
        texte_final += self.generer_phrase_synthese(res, nom_fichier)

        self.text_synthese.configure(text=texte_final)

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

import customtkinter as ctk
import os
import engine  # Indispensable pour lancer les calculs de comparaison
import sorting
from analysepage import AnalysePage


class StableMenu(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Tris Stables - Configuration")
        self.geometry("500x700")
        self.attributes("-topmost", True)

        # --- INITIALISATION DU MOTEUR ---
        self.runner = engine.BenchmarkRunner()

        # --- TITRE ---
        self.label = ctk.CTkLabel(
            self, text="ALGORITHMES STABLES", font=("Arial", 20, "bold")
        )
        self.label.pack(pady=20)

        # --- CHOIX DU FICHIER POUR LA COMPARAISON ---
        # On a besoin de savoir sur quelle liste comparer les algos !
        self.label_file = ctk.CTkLabel(self, text="Fichier pour la comparaison :")
        self.label_file.pack(pady=5)

        self.options_listes = [
            "json_data/short_rd.json",
            "json_data/short_rv.json",
            "json_data/medium_rd.json",
            "json_data/medium_rv.json",
            "json_data/large_rv.json",
            "json_data/large_rd.json",
            "json_data/xlarge_rv.json",
            "json_data/xlarge_rd.json",
        ]
        self.combo_liste = ctk.CTkComboBox(self, values=self.options_listes, width=250)
        self.combo_liste.pack(pady=5)
        self.combo_liste.set("json_data/short_rd.json")

        # --- BOUTONS INDIVIDUELS ---
        # On utilise une Frame pour grouper les boutons de tris
        self.frame_tris = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tris.pack(pady=20)

        ctk.CTkButton(
            self.frame_tris,
            text="Lancer Tri Bulle",
            command=lambda: AnalysePage(self, "Tri Bulle", sorting.TriBulle),
        ).pack(pady=5)

        ctk.CTkButton(
            self.frame_tris,
            text="Lancer Tri Insertion",
            command=lambda: AnalysePage(
                self, "Tri par Insertion", sorting.TriInsertion
            ),
        ).pack(pady=5)

        ctk.CTkButton(
            self.frame_tris,
            text="Lancer Tri Fusion",
            command=lambda: AnalysePage(self, "Tri par Fusion", sorting.TriFusion),
        ).pack(pady=5)

        # --- SEPARATEUR ---
        ctk.CTkLabel(self, text="─" * 30).pack(pady=10)

        # --- BOUTON COMPARAISON (Le nouveau !) ---
        self.btn_compare_stables = ctk.CTkButton(
            self,
            text="📊 COMPARER LES 3 STABLES",
            fg_color="#457B9D",
            hover_color="#1D3557",
            height=50,
            font=("Arial", 14, "bold"),
            command=self.afficher_comparaison_stables,
        )
        self.btn_compare_stables.pack(pady=20)

    def afficher_comparaison_stables(self):
        import matplotlib.pyplot as plt

        nom_fichier = self.combo_liste.get()
        if not os.path.exists(nom_fichier):
            print(f"Erreur : {nom_fichier} introuvable")
            return

        # 1. Préparation
        dict_stables = {
            "Tri Bulle": sorting.TriBulle,
            "Tri Insertion": sorting.TriInsertion,
            "Tri Fusion": sorting.TriFusion,
        }

        noms = []
        temps = []

        # 2. Calculs
        for nom, classe in dict_stables.items():
            self.runner.lancer(classe, nom_fichier)
            res = self.runner.resultats[-1]
            noms.append(nom)
            temps.append(res["temps"])

        # 3. Graphique
        fig, ax = plt.subplots(figsize=(8, 6))
        bars = ax.bar(noms, temps, color=["#E63946", "#1D3557", "#457B9D"])

        ax.set_ylabel("Temps en secondes")
        ax.set_title(f"Comparaison des Tris Stables\nFichier : {nom_fichier}")

        # Ajout des étiquettes au-dessus des barres
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.6f}s",
                ha="center",
                va="bottom",
                fontweight="bold",
            )

        plt.tight_layout()
        plt.show()

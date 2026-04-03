import customtkinter as ctk
import os
import engine  # Indispensable pour lancer les calculs de comparaison
import sorting
from analysepage import AnalysePage


class StableMenu(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Tris Stables - Configuration")
        self.geometry("500x750")

        # Configuration du fond pour matcher le thème sombre
        self.configure(fg_color="#101626")
        self.attributes("-topmost", True)

        # --- INITIALISATION DU MOTEUR ---
        self.runner = engine.BenchmarkRunner()

        # --- TITRE STYLE NÉON ---
        self.label = ctk.CTkLabel(
            self,
            text="ALGORITHMES STABLES",
            font=("Montserrat", 22, "bold"),
            text_color="#00FFFF",  # Cyan pour les stables
        )
        self.label.pack(pady=(30, 20))

        # --- SECTION SÉLECTION FICHIER ---
        self.file_frame = ctk.CTkFrame(
            self,
            fg_color="#1A1A1A",
            corner_radius=15,
            border_width=1,
            border_color="#333333",
        )
        self.file_frame.pack(pady=10, padx=30, fill="x")

        self.label_file = ctk.CTkLabel(
            self.file_frame,
            text="Fichier pour la comparaison :",
            font=("Arial", 12),
            text_color="#707070",
        )
        self.label_file.pack(pady=(10, 0))

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
        self.combo_liste = ctk.CTkComboBox(
            self.file_frame,
            values=self.options_listes,
            width=300,
            fg_color="#2B2B2B",
            border_color="#00FFFF",
            button_color="#00FFFF",
            corner_radius=10,
        )
        self.combo_liste.pack(pady=15)
        self.combo_liste.set("json_data/short_rd.json")

        # --- BOUTONS INDIVIDUELS ---
        self.frame_tris = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tris.pack(pady=20)

        # Style commun pour les boutons de tris
        btn_style = {
            "width": 280,
            "height": 45,
            "font": ("Arial", 14, "bold"),
            "fg_color": "#2B2B2B",
            "hover_color": "#3D3D3D",
            "border_width": 1,
            "border_color": "#444444",
        }

        ctk.CTkButton(
            self.frame_tris,
            text="Lancer Tri Bulle",
            command=lambda: AnalysePage(self, "Tri Bulle", sorting.TriBulle),
            **btn_style,
        ).pack(pady=10)

        ctk.CTkButton(
            self.frame_tris,
            text="Lancer Tri Insertion",
            command=lambda: AnalysePage(
                self, "Tri par Insertion", sorting.TriInsertion
            ),
            **btn_style,
        ).pack(pady=10)

        ctk.CTkButton(
            self.frame_tris,
            text="Lancer Tri Fusion",
            command=lambda: AnalysePage(self, "Tri par Fusion", sorting.TriFusion),
            **btn_style,
        ).pack(pady=10)

        # --- SÉPARATEUR VISUEL ---
        self.separator = ctk.CTkFrame(self, height=2, fg_color="#333333", width=400)
        self.separator.pack(pady=20)

        # --- BOUTON COMPARAISON ---
        self.btn_compare_stables = ctk.CTkButton(
            self,
            text="📊 COMPARER LES 3 STABLES",
            fg_color="#00FFFF",
            text_color="#101626",  # Texte sombre sur fond clair
            hover_color="#00CCCC",
            height=60,
            width=350,
            font=("Arial", 16, "bold"),
            corner_radius=15,
            command=self.afficher_comparaison_stables,
        )
        self.btn_compare_stables.pack(pady=20)

    def afficher_comparaison_stables(self):
        import matplotlib.pyplot as plt
        import matplotlib as mpl

        # Application du style sombre au graphique de comparaison pour rester dans le thème
        mpl.rcParams.update(
            {
                "figure.facecolor": "#101626",
                "axes.facecolor": "#101626",
                "axes.edgecolor": "#3A4561",
                "axes.labelcolor": "white",
                "xtick.color": "white",
                "ytick.color": "white",
                "text.color": "white",
            }
        )

        nom_fichier = self.combo_liste.get()
        if not os.path.exists(nom_fichier):
            print(f"Erreur : {nom_fichier} introuvable")
            return

        dict_stables = {
            "Tri Bulle": sorting.TriBulle,
            "Tri Insertion": sorting.TriInsertion,
            "Tri Fusion": sorting.TriFusion,
        }

        noms, temps = [], []
        for nom, classe in dict_stables.items():
            self.runner.lancer(classe, nom_fichier)
            res = self.runner.resultats[-1]
            noms.append(nom)
            temps.append(res["temps"])

        fig, ax = plt.subplots(figsize=(8, 6))
        # Palette néon pour les barres
        colors = ["#00FFFF", "#39FF14", "#FF00FF"]
        bars = ax.bar(noms, temps, color=colors, alpha=0.8)

        ax.set_ylabel("Temps en secondes", fontsize=12)
        ax.set_title(
            f"Benchmark Tris Stables\nFichier : {os.path.basename(nom_fichier)}",
            fontsize=14,
            pad=20,
        )
        ax.grid(axis="y", linestyle=":", alpha=0.3)

        # Étiquettes de données
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.6f}s",
                ha="center",
                va="bottom",
                fontweight="bold",
                color="white",
            )

        plt.tight_layout()
        plt.show()

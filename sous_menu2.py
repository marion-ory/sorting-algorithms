import customtkinter as ctk
import os
import engine  # Importation du moteur de benchmark
import sorting  # Importation des classes de tri
from analysepage import AnalysePage

# Import des classes spécifiques
from sorting import TriPeigne, TriSelection, TriRapide, TriTas


class InstableMenu(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Tris Instables - Configuration")
        self.geometry("500x780")  # Un peu plus grand pour l'élégance

        # Configuration du fond (Dark profond)
        self.configure(fg_color="#101626")
        self.attributes("-topmost", True)

        # --- INITIALISATION DU MOTEUR ---
        self.runner = engine.BenchmarkRunner()

        # --- TITRE STYLE NÉON MAGENTA ---
        self.label = ctk.CTkLabel(
            self,
            text="ALGORITHMES INSTABLES",
            font=("Montserrat", 22, "bold"),
            text_color="#FF00FF",  # Magenta pour différencier des stables (Cyan)
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
            text="Choisir le fichier pour comparer :",
            font=("Arial", 12),
            text_color="#707070",
        )
        self.label_file.pack(pady=(10, 0))

        self.options_listes = [
            "json_data/short_rd.json",
            "json_data/short_rv.json",
            "json_data/medium_rd.json",
            "json_data/medium_rv.json",
            "json_data/large_rd.json",
            "json_data/large_rv.json",
        ]
        self.combo_liste = ctk.CTkComboBox(
            self.file_frame,
            values=self.options_listes,
            width=300,
            fg_color="#2B2B2B",
            border_color="#FF00FF",  # Bordure Magenta
            button_color="#FF00FF",
            corner_radius=10,
        )
        self.combo_liste.pack(pady=15)
        self.combo_liste.set("json_data/short_rd.json")

        # --- BOUTONS INDIVIDUELS ---
        self.frame_individuel = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_individuel.pack(pady=20)

        # Style commun pour les boutons (Épuré)
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
            self.frame_individuel,
            text="Lancer Tri Peigne",
            command=lambda: AnalysePage(self, "Tri à Peigne", TriPeigne),
            **btn_style,
        ).pack(pady=8)
        ctk.CTkButton(
            self.frame_individuel,
            text="Lancer Tri Rapide",
            command=lambda: AnalysePage(self, "Tri Rapide", TriRapide),
            **btn_style,
        ).pack(pady=8)
        ctk.CTkButton(
            self.frame_individuel,
            text="Lancer Tri Sélection",
            command=lambda: AnalysePage(self, "Tri par Sélection", TriSelection),
            **btn_style,
        ).pack(pady=8)
        ctk.CTkButton(
            self.frame_individuel,
            text="Lancer Tri par Tas",
            command=lambda: AnalysePage(self, "Tri par Tas", TriTas),
            **btn_style,
        ).pack(pady=8)

        # --- SÉPARATEUR ---
        self.separator = ctk.CTkFrame(self, height=2, fg_color="#333333", width=400)
        self.separator.pack(pady=20)

        # --- BOUTON COMPARAISON (EFFET CORAIL/MAGENTA) ---
        self.btn_compare_instables = ctk.CTkButton(
            self,
            text="📊 COMPARER LES 4 INSTABLES",
            fg_color="#FF00FF",  # Magenta vibrant
            text_color="#101626",  # Texte sombre pour lisibilité
            hover_color="#CC00CC",
            height=60,
            width=350,
            font=("Arial", 16, "bold"),
            corner_radius=15,
            command=self.afficher_comparaison_instables,
        )
        self.btn_compare_instables.pack(pady=20)

    def afficher_comparaison_instables(self):
        import matplotlib.pyplot as plt
        import matplotlib as mpl

        # Application du style sombre au graphique
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

        dict_instables = {
            "Tas": TriTas,
            "Peigne": TriPeigne,
            "Rapide": TriRapide,
            "Sélection": TriSelection,
        }

        noms, temps = [], []
        for nom, classe in dict_instables.items():
            self.runner.lancer(classe, nom_fichier)
            res = self.runner.resultats[-1]
            noms.append(nom)
            temps.append(res["temps"])

        fig, ax = plt.subplots(figsize=(8, 6))
        # Palette de couleurs "Sunset/Néon"
        couleurs = ["#FF00FF", "#FF7000", "#FFD700", "#FF4500"]
        bars = ax.bar(noms, temps, color=couleurs, alpha=0.8)

        ax.set_ylabel("Temps en secondes", fontsize=12)
        ax.set_title(
            f"Benchmark Tris Instables\nFichier : {os.path.basename(nom_fichier)}",
            fontsize=14,
            pad=20,
        )
        ax.grid(axis="y", linestyle=":", alpha=0.3)

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

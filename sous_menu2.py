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
        self.geometry("500x750")  # Augmenté pour laisser de la place au combo

        # S'assurer que la fenêtre passe devant
        self.attributes("-topmost", True)

        # --- INITIALISATION DU MOTEUR (INDISPENSABLE) ---
        self.runner = engine.BenchmarkRunner()

        # --- TITRE ---
        self.label = ctk.CTkLabel(
            self, text="ALGORITHMES INSTABLES", font=("Arial", 20, "bold")
        )
        self.label.pack(pady=20)

        # --- CHOIX DU FICHIER POUR LA COMPARAISON ---
        self.label_file = ctk.CTkLabel(self, text="Choisir le fichier pour comparer :")
        self.label_file.pack(pady=5)

        self.options_listes = [
            "json_data/short_rd.json",
            "json_data/short_rv.json",
            "json_data/medium_rd.json",
            "json_data/medium_rv.json",
            "json_data/large_rd.json",
            "json_data/large_rv.json",
        ]
        self.combo_liste = ctk.CTkComboBox(self, values=self.options_listes, width=300)
        self.combo_liste.pack(pady=5)
        self.combo_liste.set("json_data/short_rd.json")

        # --- BOUTONS INDIVIDUELS ---
        self.frame_individuel = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_individuel.pack(pady=20)

        # Tri à Peigne
        ctk.CTkButton(
            self.frame_individuel,
            text="Lancer Tri Peigne",
            command=lambda: AnalysePage(self, "Tri à Peigne", TriPeigne),
        ).pack(pady=10)

        # Tri Rapide
        ctk.CTkButton(
            self.frame_individuel,
            text="Lancer Tri Rapide",
            command=lambda: AnalysePage(self, "Tri Rapide", TriRapide),
        ).pack(pady=10)

        # Tri par Sélection
        ctk.CTkButton(
            self.frame_individuel,
            text="Lancer Tri Sélection",
            command=lambda: AnalysePage(self, "Tri par Sélection", TriSelection),
        ).pack(pady=10)

        # Tri par Tas
        ctk.CTkButton(
            self.frame_individuel,
            text="Lancer Tri par Tas",
            command=lambda: AnalysePage(self, "Tri par Tas", TriTas),
        ).pack(pady=10)

        # --- BOUTON COMPARAISON ---
        self.btn_compare_instables = ctk.CTkButton(
            self,
            text="📊 COMPARER LES 4 INSTABLES",
            fg_color="#E76F51",  # Couleur corail pour les instables
            hover_color="#A34D37",
            height=50,
            font=("Arial", 14, "bold"),
            command=self.afficher_comparaison_instables,
        )
        self.btn_compare_instables.pack(pady=20)

    def afficher_comparaison_instables(self):
        import matplotlib.pyplot as plt

        nom_fichier = self.combo_liste.get()
        if not os.path.exists(nom_fichier):
            print(f"Erreur : {nom_fichier} introuvable")
            return

        # 1. Préparation (Correction des références aux classes)
        dict_instables = {
            "Tas": TriTas,
            "Peigne": TriPeigne,
            "Rapide": TriRapide,
            "Sélection": TriSelection,
        }

        noms = []
        temps = []

        # 2. Calculs (Utilisation de self.runner)
        for nom, classe in dict_instables.items():
            self.runner.lancer(classe, nom_fichier)
            res = self.runner.resultats[-1]
            noms.append(nom)
            temps.append(res["temps"])

        # 3. Graphique
        fig, ax = plt.subplots(figsize=(8, 6))
        # 4 couleurs pour 4 barres
        couleurs = ["#E76F51", "#F4A261", "#E9C46A", "#2A9D8F"]
        bars = ax.bar(noms, temps, color=couleurs)

        ax.set_ylabel("Temps en secondes")
        ax.set_title(
            f"Comparaison des Tris Instables\nFichier : {os.path.basename(nom_fichier)}"
        )

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

import customtkinter as ctk
import json
import os
import time
import psutil  # Pour la RAM (pense à faire : pip install psutil)


class AnalysePage(ctk.CTkToplevel):
    def __init__(self, parent, nom_algo, fonction_tri):
        super().__init__(parent)
        self.title(f"Analyse Performance - {nom_algo}")
        self.geometry("600x750")

        # On stocke l'algorithme reçu en paramètre
        self.fonction_tri = fonction_tri
        self.nom_algo = nom_algo

        # --- TITRE DYNAMIQUE ---
        self.label_titre = ctk.CTkLabel(
            self, text=f"ANALYSE : {nom_algo}", font=("Arial", 22, "bold")
        )
        self.label_titre.pack(pady=20)

        # --- ZONE AFFICHAGE (Menu déroulant + Liste) ---
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
            text="LANCER LE TIMER & RAM",
            fg_color="#2A9D8F",
            height=40,
            font=("Arial", 14, "bold"),
            command=self.executer_mesures,
        )
        self.btn_run.pack(pady=20)

        # --- RÉSULTATS BRUTS (STATS) ---
        self.stats_box = ctk.CTkTextbox(
            self, width=500, height=150, font=("Courier", 13)
        )
        self.stats_box.pack(pady=10)

        # --- ZONE DE SYNTHÈSE (LA PHRASE EXPLICATIVE) ---
        self.frame_synthese = ctk.CTkFrame(self, fg_color="#333333", corner_radius=15)
        self.frame_synthese.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_synthese_titre = ctk.CTkLabel(
            self.frame_synthese, text="SYNTHÈSE DU TRI", font=("Arial", 14, "italic")
        )
        self.label_synthese_titre.pack(pady=5)

        self.text_synthese = ctk.CTkLabel(
            self.frame_synthese,
            text="En attente de calcul...",
            wraplength=450,
            font=("Arial", 13),
        )
        self.text_synthese.pack(pady=15, padx=20)

    def executer_mesures(self):
        nom_fichier = self.combo_liste.get()

        # 1. Chargement du fichier
        try:
            with open(nom_fichier, "r") as f:
                liste_test = json.load(f)
        except Exception as e:
            self.stats_box.insert("0.0", f"Erreur chargement : {e}")
            return

        # 2. Mesures (RAM + TEMPS)
        process = psutil.Process(os.getpid())
        mem_avant = process.memory_info().rss / (1024 * 1024)  # Conversion en MB

        start_time = time.time()
        self.fonction_tri(liste_test)  # On exécute l'algo
        end_time = time.time()

        mem_apres = process.memory_info().rss / (1024 * 1024)

        temps_final = end_time - start_time
        conso_ram = max(0, mem_apres - mem_avant)

        # 3. Affichage des Statistiques
        self.stats_box.delete("0.0", "end")
        stats = f"--- RÉSULTATS {self.nom_algo.upper()} ---\n"
        stats += f"Fichier utilisé : {nom_fichier}\n"
        stats += f"Taille liste    : {len(liste_test)} éléments\n"
        stats += f"Temps d'exécution: {temps_final:.6f} sec\n"
        stats += f"Mémoire utilisée : {conso_ram:.2f} MB\n"
        self.stats_box.insert("0.0", stats)

        # 4. Génération de la phrase de synthèse (L'intelligence du code)
        type_liste = "désordonnée" if "_rd" in nom_fichier else "inversée (pire cas)"
        vitesse = (
            "ultra-rapide"
            if temps_final < 0.01
            else "efficace" if temps_final < 0.5 else "coûteuse en temps"
        )

        phrase = f"L'analyse montre que pour une liste {type_liste} de {len(liste_test)} valeurs, "
        phrase += f"le {self.nom_algo} s'est révélé {vitesse}. "

        if conso_ram > 1:
            phrase += f"\nOn note une consommation RAM de {conso_ram:.2f} MB, ce qui est typique des algos récursifs ou créant des copies."
        else:
            phrase += "\nL'impact sur la mémoire vive est négligeable (tri 'in-place')."

        self.text_synthese.configure(text=phrase)

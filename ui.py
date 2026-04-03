import customtkinter as ctk
import os

from graphic_ram import GraphRAM
from graphic_tous import GraphicTous
from sous_menu import StableMenu
from sous_menu2 import InstableMenu

# --- CONFIGURATION DU THÈME GLOBAL ---
ctk.set_appearance_mode("dark")  # Mode sombre forcé
ctk.set_default_color_theme("blue")  # Thème de base


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Algorithme de Tri - Menu Principal")
        self.geometry("600x650")  # Un peu plus haut pour l'élégance

        # Configuration de la grille pour centrer les éléments
        self.grid_columnconfigure(0, weight=1)

        # --- TITRE PRINCIPAL STYLE NÉON ---
        self.label = ctk.CTkLabel(
            self,
            text="ALGORITHMES DE TRI",
            font=("Montserrat", 32, "bold"),
            text_color="#00FFFF",  # Cyan Néon
        )
        self.label.pack(pady=(50, 10))

        self.sub_label = ctk.CTkLabel(
            self,
            text="Analyse de Performance & Complexité",
            font=("Arial", 14, "italic"),
            text_color="#707070",
        )
        self.sub_label.pack(pady=(0, 30))

        # --- CONTENEUR DES BOUTONS AVEC EFFET DE CADRE ---
        self.button_frame = ctk.CTkFrame(
            self,
            fg_color="#1A1A1A",  # Gris très sombre
            border_width=2,
            border_color="#333333",
            corner_radius=20,
        )
        self.button_frame.pack(pady=10, padx=50, fill="x")

        # Bouton TRI STABLE
        self.btn_stable = ctk.CTkButton(
            self.button_frame,
            text="TRI STABLE",
            width=250,
            height=60,
            font=("Arial", 18, "bold"),
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            border_width=1,
            border_color="#00FFFF",  # Bordure Cyan
            command=self.ouvrir_menu_stable,
        )
        self.btn_stable.pack(pady=20, padx=20)

        # Bouton TRI INSTABLE
        self.btn_instable = ctk.CTkButton(
            self.button_frame,
            text="TRI INSTABLE",
            width=250,
            height=60,
            font=("Arial", 18, "bold"),
            fg_color="#2B2B2B",
            hover_color="#3D3D3D",
            border_width=1,
            border_color="#FF00FF",  # Bordure Magenta
            command=self.ouvrir_menu_instable,
        )
        self.btn_instable.pack(pady=20, padx=20)

        # --- BOUTON COMPARAISON COMPLEXITE (DASHBOARD) ---
        # On le détache visuellement car c'est la fonction "Premium"
        self.btn_compare_tous = ctk.CTkButton(
            self,
            text=" DASHBOARD COMPARATIF GLOBAL",
            fg_color="#E76F51",  # Orange corail
            hover_color="#A34D37",
            width=400,
            height=70,
            corner_radius=15,
            font=("Arial", 16, "bold"),
            command=self.ouvrir_menu_comparaison_tous,
        )
        self.btn_compare_tous.pack(pady=40)

        # Petit rappel de copyright ou version en bas
        self.footer = ctk.CTkLabel(
            self,
            text="v2.0 - Dashboard Edition",
            font=("Arial", 10),
            text_color="#404040",
        )
        self.footer.pack(side="bottom", pady=10)

    def ouvrir_menu_stable(self):
        self.nouvelle_fenetre = StableMenu(self)
        self.nouvelle_fenetre.focus()

    def ouvrir_menu_instable(self):
        self.nouvelle_fenetre = InstableMenu(self)
        self.nouvelle_fenetre.focus()

    def ouvrir_menu_comparaison_tous(self):
        """Lance la fenêtre des courbes de complexité."""
        try:
            # On instancie la classe du fichier Graphic_tous.py
            self.nouvelle_fenetre = GraphicTous(self)
        except Exception as e:
            print(f"Erreur lors de l'ouverture du graphique : {e}")

    def ouvrir_menu_ram(self):
        try:
            self.nouvelle_fenetre = GraphRAM(self)
        except Exception as e:
            print(f"Erreur lors de l'ouverture du graphique : {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()

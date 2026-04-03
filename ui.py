import customtkinter as ctk
import os


from graphic_tous import GraphicTous
from sous_menu import StableMenu
from sous_menu2 import InstableMenu


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Algorithme de Tri - Menu Principal")
        self.geometry("600x600")  # Un peu plus grand pour tout caser

        # Titre Principal
        self.label = ctk.CTkLabel(
            self, text="ALGORITHMES DE TRI", font=("Arial", 28, "bold")
        )
        self.label.pack(pady=40)

        # Conteneur des boutons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        # Bouton TRI STABLE
        self.btn_stable = ctk.CTkButton(
            self.button_frame,
            text="TRI STABLE",
            width=250,
            height=60,
            font=("Arial", 18),
            command=self.ouvrir_menu_stable,
        )
        self.btn_stable.pack(pady=15)

        # Bouton TRI INSTABLE
        self.btn_instable = ctk.CTkButton(
            self.button_frame,
            text="TRI INSTABLE",
            width=250,
            height=60,
            font=("Arial", 18),
            command=self.ouvrir_menu_instable,
        )
        self.btn_instable.pack(pady=15)

        # --- BOUTON COMPARAISON GÉNÉRALE ---
        self.btn_compare_tous = ctk.CTkButton(
            self,
            text="📈 COURBES DE COMPLEXITÉ (TOUS)",
            fg_color="#E76F51",
            hover_color="#A34D37",
            width=350,
            height=60,
            font=("Arial", 14, "bold"),
            command=self.ouvrir_menu_comparaison_tous,
        )
        self.btn_compare_tous.pack(pady=30)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()

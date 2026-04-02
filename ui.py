import customtkinter as ctk
import subprocess
from sous_menu import StableMenu
from sous_menu2 import InstableMenu
from analysepage import AnalysePage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Algorithme de Tri - Menu Principal")
        self.geometry("600x500")

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

        # Bouton VISUALISATION (Lien direct vers ton graphic.py)
        self.btn_visu = ctk.CTkButton(
            self.button_frame,
            text="VISUALISATION GRAPHIQUE",
            width=250,
            height=60,
            font=("Arial", 18),
            fg_color="#7B2CBF",
            hover_color="#5A189A",
            command=self.lancer_graphic_py,
        )
        self.btn_visu.pack(pady=15)

    def lancer_graphic_py(self):
        # Lance ton script de visualisation circulaire
        subprocess.Popen(["python3", "graphic.py"])

    def ouvrir_menu_stable(self):
        print("Ouverture du menu des Tris Stables...")
        # Ici tu créeras une nouvelle fenêtre ou tu changeras le contenu de celle-ci

    def ouvrir_menu_instable(self):
        print("Ouverture du menu des Tris Instables...")
        # Idem pour les Tris Instables

    def ouvrir_menu_stable(self):
        # On crée une instance de la fenêtre définie dans sous_menu.py
        self.nouvelle_fenetre = StableMenu(self)
        # On la met au premier plan
        self.nouvelle_fenetre.focus()

    def ouvrir_menu_instable(self):
        # On crée une instance de la fenêtre définie dans sous_menu.py
        self.nouvelle_fenetre = InstableMenu(self)
        # On la met au premier plan
        self.nouvelle_fenetre.focus()


if __name__ == "__main__":
    app = App()
    app.mainloop()

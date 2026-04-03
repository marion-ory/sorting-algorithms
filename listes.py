import json
import random
import os


def generer_listes():
    # 1. Sécurité : Créer le dossier s'il n'existe pas
    if not os.path.exists("json_data"):
        os.makedirs("json_data")
        print("📁 Dossier 'json_data' créé.")

    # Configuration des tailles
    tailles = {"short": 30, "medium": 1000, "large": 5000, "xlarge": 6000}

    for nom, taille in tailles.items():
        # --- GÉNÉRATION DE LA LISTE ALÉATOIRE ---

        # On génère (taille - 2) nombres uniques
        liste_rd = random.sample(range(1, 1000000), taille - 2)

        # On choisit deux nombres au hasard dans cette liste pour créer les doublons
        valeur_doublon1 = random.choice(liste_rd)
        valeur_doublon2 = random.choice(liste_rd)

        # On les ajoute à la liste
        liste_rd.append(valeur_doublon1)
        liste_rd.append(valeur_doublon2)

        # On mélange
        random.shuffle(liste_rd)

        # --- GÉNÉRATION DE LA LISTE INVERSÉE (PIRE CAS) ---
        liste_rv = sorted(liste_rd, reverse=True)

        # --- SAUVEGARDE EN JSON ---

        # Liste Aléatoire (Random Data -> _rd)
        with open(f"json_data/{nom}_rd.json", "w") as f:
            json.dump(liste_rd, f)

        # Liste Inversée (Reverse Data -> _rv)
        # CORRECTION : ajout du 'f', du mode 'w' et changement du nom en _rv
        with open(f"json_data/{nom}_rv.json", "w") as f:
            json.dump(liste_rv, f)

        print(f"✅ Listes '{nom}' générées ({taille} éléments).")


if __name__ == "__main__":
    generer_listes()

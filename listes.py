import json
import random


def generer_listes():
    # Configuration des tailles
    tailles = {"short": 30, "medium": 100, "large": 1000, "xlarge": 6000}

    for nom, taille in tailles.items():
        # --- GÉNÉRATION DE LA LISTE ALÉATOIRE ---

        # On génère d'abord (taille - 2) nombres uniques
        # L'intervalle est large pour éviter les collisions naturelles
        liste_rd = random.sample(range(1, 1000000), taille - 2)

        # On choisit deux nombres au hasard dans cette liste pour créer les doublons
        valeur_doublon1 = random.choice(liste_rd)
        valeur_doublon2 = random.choice(liste_rd)

        # On les ajoute à la liste pour atteindre la taille finale
        liste_rd.append(valeur_doublon1)
        liste_rd.append(valeur_doublon2)

        # On mélange pour que les doublons ne soient pas à la fin
        random.shuffle(liste_rd)

        # --- GÉNÉRATION DE LA LISTE INVERSÉE (PIRE CAS) ---
        liste_rv = sorted(liste_rd, reverse=True)

        # Sauvegarde en JSON
        with open(f"json_data/{nom}_rd.json", "w") as f:
            json.dump(liste_rd, f)

        with open("json_data/{nom}_rd.json") as f:
            json.dump(liste_rv, f)


if __name__ == "__main__":
    generer_listes()

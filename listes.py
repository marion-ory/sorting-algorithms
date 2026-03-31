import random
import json

taille = {"short": 1000, "medium": 20000, "large": 200000, "xlarge": 1000000}


def generer_liste():
    #                     [ RANDOM ]
    short = [random.randint(0, 100) for _ in range(taille["short"])]

    medium = [random.randint(0, 2000) for _ in range(taille["medium"])]

    large = [random.randint(0, 200000) for _ in range(taille["large"])]

    xlarge = [random.randint(0, 1000000) for _ in range(taille["xlarge"])]

    #                           [ RANDOM INVERSE ]

    short_reverse = sorted(short.copy(), reverse=True)
    medium_reverse = sorted(medium.copy(), reverse=True)
    large_reverse = sorted(large.copy(), reverse=True)
    xlarge_reverse = sorted(xlarge.copy(), reverse=True)

    #                            [SAUVEGARDE JSON ]

    fichiers = {
        "short_rd.json": short,
        "medium_rd.json": medium,
        "large_rd.json": large,
        "xlarge_rd.json": xlarge,
        "short_rv.json": short_reverse,
        "medium_rv.json": medium_reverse,
        "large_rv.json": large_reverse,
        "xlarge_rv.json": xlarge_reverse,
    }

    for nom_fichier, donnees in fichiers.items():
        with open(nom_fichier, "w") as f:
            json.dump(donnees, f)


if __name__ == "__main__":
    generer_liste()

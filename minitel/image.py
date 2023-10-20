from minitel.constants import *

def _huit_niveaux(niveau):
    # Niveau peut soit être un tuple soit un entier
    # Gère les deux cas en testant l’exception
    try:
        return niveau * 8 / 256
    except TypeError:
        return int(
            round(
                sqrt(
                    0.299 * niveau[0] ** 2 +
                    0.587 * niveau[1] ** 2 +
                    0.114 * niveau[2] ** 2
                )
            ) * 8 / 256
        )

def _deux_couleurs(couleurs):
    assert isinstance(couleurs, list)

    # Crée une liste contenant le nombre de fois où un niveau est
    # enregistré
    niveaux = [0, 0, 0, 0, 0, 0, 0, 0]

    # Passe en revue tous les niveaux pour les comptabiliser
    for couleur in couleurs:
        niveaux[couleur] += 1

    # Prépare la liste des niveaux afin de pouvoir la trier du plus
    # utilisé au moins utilisé. Pour cela, on crée une liste de tuples
    # (niveau, nombre d’apparitions)
    niveaux = [(index, valeur) for index, valeur in enumerate(niveaux)]

    # Trie les niveaux par nombre d’apparition
    niveaux = sorted(niveaux, key = itemgetter(1), reverse = True)

    # Retourne les deux niveaux les plus rencontrés
    return (niveaux[0][0], niveaux[1][0])

def _arp_ou_avp(couleur, arp, avp):
    assert isinstance(couleur, int)
    assert isinstance(arp, int)
    assert isinstance(avp, int)

    if(abs(arp - couleur) < abs(avp - couleur)):
        return 0

    return 1


def image2minitel(img):
    assert image.size[0] <= 80
    assert image.size[0] <= 72

    # En mode semi-graphique, un caractère a 2 pixels de largeur
    # et 3 pixels de hauteur
    charWidth = int(image.size[0] / 2)
    charHeight = int(image.size[1] / 3)

    output = tMoveCursor + tLine(1) + tCol(1)

    for h in range(0, charHeight):
        output = output + b'\x0e'  # mode semi graphique
        for w in range(0, charWidth):
            pixels = [img.getpixel((2*w + x, h*3 + y)) for x in range(2) for y in range(3)]
            

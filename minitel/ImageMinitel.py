#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ImageMinitel est une classe permettant de convertir une image lisible par
PIL en semi-graphiques pour le Minitel.

"""

from operator import itemgetter

from math import sqrt
from unicodedata import normalize
from binascii import unhexlify

ESC = 0x1b # escape
SO  = 0x0e # shift out
DC2 = 0x12 # device control 2
# Les niveaux de gris s’échelonnent comme suit :
# nor, bleu, rouge, magenta, vert, cyan, jaune, blanc
COULEURS_MINITEL = {
    'noir': 0, 'rouge': 1, 'vert': 2, 'jaune': 3,
    'bleu': 4, 'magenta': 5, 'cyan': 6, 'blanc': 7,
    '0': 0, '1': 4, '2': 1, '3': 5,
    '4': 2, '5': 6, '6': 3, '7': 7,
    0: 0, 1: 4, 2: 1, 3: 5,
    4: 2, 5: 6, 6: 3, 7: 7
}


# Tables de conversion des caractères spéciaux
UNICODEVERSVIDEOTEX = {
    '£': '1923', '°': '1930', '±': '1931', 
    '←': '192C', '↑': '192D', '→': '192E', '↓': '192F', 
    '¼': '193C', '½': '193D', '¾': '193E', 
    'ç': '194B63', '’': '194B27', 
    'à': '194161', 'á': '194261', 'â': '194361', 'ä': '194861', 
    'è': '194165', 'é': '194265', 'ê': '194365', 'ë': '194865', 
    'ì': '194169', 'í': '194269', 'î': '194369', 'ï': '194869', 
    'ò': '19416F', 'ó': '19426F', 'ô': '19436F', 'ö': '19486F', 
    'ù': '194175', 'ú': '194275', 'û': '194375', 'ü': '194875', 
    'Œ': '196A', 'œ': '197A', 
    'ß': '197B', 'β': '197B'
}

UNICODEVERSAUTRE = {
    '£': '0E230F',
    '°': '0E5B0F', 'ç': '0E5C0F', '’': '27', '`': '60', '§': '0E5D0F',
    'à': '0E400F', 'è': '0E7F0F', 'é': '0E7B0F', 'ù': '0E7C0F'
}

class Sequence:
    """Une classe représentant une séquence de valeurs

    Une Séquence est une suite de valeurs prêtes à être envoyées à un Minitel.
    Ces valeurs respectent la norme ASCII.
    """
    def __init__(self, valeur = None, standard = 'VIDEOTEX'):
        """Constructeur de Sequence

        :param valeur:
            valeur à ajouter à la construction de l’objet. Si la valeur est à
            None, aucune valeur n’est ajoutée
        :type valeur:
            une chaîne de caractères, un entier, une liste, une séquence ou
            None

        :param standard:
            standard à utiliser pour la conversion unicode vers Minitel. Les
            valeurs possibles sont VIDEOTEX, MIXTE et TELEINFORMATIQUE (la
            casse est importante)
        :type standard:
            une chaîne de caractères
        """
        assert valeur == None or \
                isinstance(valeur, (list, int, str, Sequence))
        assert standard in ['VIDEOTEX', 'MIXTE', 'TELEINFORMATIQUE']

        self.valeurs = []
        self.longueur = 0
        self.standard = standard

        if valeur != None:
            self.ajoute(valeur)
        
    def ajoute(self, valeur):
        """Ajoute une valeur ou une séquence de valeurs

        La valeur soumise est d’abord canonisée par la méthode canonise avant
        d’être ajoutée à la séquence. Cela garantit que la séquence ne contient
        que des entiers représentant des caractères de la norme ASCII.

        :param valeur:
            valeur à ajouter
        :type valeur:
            une chaîne de caractères, un entier, une liste ou une Séquence
        """
        assert isinstance(valeur, (list, int, str, Sequence))

        self.valeurs += self.canonise(valeur)
        self.longueur = len(self.valeurs)

    def canonise(self, valeur):
        """Canonise une séquence de caractères

        Si une liste est soumise, quelle que soit sa profondeur, elle sera
        remise à plat. Une liste peut donc contenir des chaînes de caractères,
        des entiers ou des listes. Cette facilité permet la construction de
        séquences de caractères plus aisée. Cela facilite également la
        comparaison de deux séquences.

        :param valeur:
            valeur à canoniser
        :type valeur:
            une chaîne de caractères, un entier, une liste ou une Séquence

        :returns:
            Une liste de profondeur 1 d’entiers représentant des valeurs à la
            norme ASCII.

        Exemple::
            canonise(['dd', 32, ['dd', 32]]) retournera
            [100, 100, 32, 100, 100, 32]
        """
        assert isinstance(valeur, (list, int, str, Sequence))

        # Si la valeur est juste un entier, on le retient dans une liste
        if isinstance(valeur, int):
            return [valeur]

        # Si la valeur est une Séquence, ses valeurs ont déjà été canonisées
        if isinstance(valeur, Sequence):
            return valeur.valeurs

        # À ce point, le paramètre contient soit une chaîne de caractères, soit
        # une liste. L’une ou l’autre est parcourable par une boucle for ... in
        # Transforme récursivement chaque élément de la liste en entier
        canonise = []
        for element in valeur:
            if isinstance(element, str):
                # Cette boucle traite 2 cas : celui ou liste est une chaîne
                # unicode et celui ou element est une chaîne de caractères
                for caractere in element:
                    for ascii in self.unicode_vers_minitel(caractere):
                        canonise.append(ascii)
            elif isinstance(element, int):
                # Un entier a juste besoin d’être ajouté à la liste finale
                canonise.append(element)
            elif isinstance(element, list):
                # Si l’élément est une liste, on la canonise récursivement
                canonise = canonise + self.canonise(element)

        return canonise

    def unicode_vers_minitel(self, caractere):
        """Convertit un caractère unicode en son équivalent Minitel

        :param caractere:
            caractère à convertir
        :type valeur:
            une chaîne de caractères unicode

        :returns:
            une chaîne de caractères contenant une suite de caractères à
            destination du Minitel.
        """
        assert isinstance(caractere, str) and len(caractere) == 1

        if self.standard == 'VIDEOTEX':
            if caractere in UNICODEVERSVIDEOTEX:
                return unhexlify(UNICODEVERSVIDEOTEX[caractere])
        else:
            if caractere in UNICODEVERSAUTRE:
                return unhexlify(UNICODEVERSAUTRE[caractere])

        return normalize('NFKD', caractere).encode('ascii', 'replace')

    def egale(self, sequence):
        """Teste l’égalité de 2 séquences

        :param sequence:
            séquence à comparer. Si la séquence n’est pas un objet Sequence,
            elle est d’abord convertie en objet Sequence afin de canoniser ses
            valeurs.
        :type sequence:
            un objet Sequence, une liste, un entier, une chaîne de caractères
            ou une chaîne unicode

        :returns:
            True si les 2 séquences sont égales, False sinon
        """
        assert isinstance(sequence, (Sequence, list, int, str))

        # Si la séquence à comparer n’est pas de la classe Sequence, alors
        # on la convertit
        if not isinstance(sequence, Sequence):
            sequence = Sequence(sequence)

        return self.valeurs == sequence.valeurs

    def __repr__(self):
        """Represente une sequence comme chaine de caracteres.

        :returns:
          Une chaine representant la sequence
        """
        return "Sequence(%s)" % self.valeurs



def _huit_niveaux(niveau):
    """Convertit un niveau sur 8 bits (256 valeurs possibles) en un niveau
    sur 3 bits (8 valeurs possibles).

    :param niveau:
        Niveau à convertir. Si c’est un tuple qui est fourni, la luminosité de
        la couleur est alors calculée. La formule est issue de la page
        http://alienryderflex.com/hsp.html
    :type niveau:
        un tuple ou un entier

    :returns:
        Un entier compris entre 0 et 7 inclus.
    """
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
    """Réduit une liste de couleurs à un couple de deux couleurs.

    Les deux couleurs retenues sont les couleurs les plus souvent
    présentes.

    :param couleurs:
        Les couleurs à réduire. Chaque couleur doit être un entier compris
        entre 0 et 7 inclus.
    :type couleurs:
        Une liste d’entiers

    :returns:
        Un tuple de deux entiers représentant les couleurs sélectionnées.
    """
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
    """Convertit une couleur en couleur d’arrière-plan ou d’avant-plan.

    La conversion se fait en calculant la proximité de la couleur avec la
    couleur d’arrière-plan (arp) et avec la couleur d’avant-plan (avp).

    :param couleur:
        La couleur à convertir (valeur de 0 à 7 inclus).
    :type couleur:
        un entier

    :param arp:
        La couleur d’arrière-plan (valeur de 0 à 7 inclus)
    :type arp:
        un entier

    :param avp:
        La couleur d’avant-plan (valeur de 0 à 7 inclus)
    :type avp:
        un entier

    :returns:
        0 si la couleur est plus proche de la couleur d’arrière-plan, 1 si
        la couleur est plus proche de la couleur d’avant-plan.
    """
    assert isinstance(couleur, int)
    assert isinstance(arp, int)
    assert isinstance(avp, int)

    if(abs(arp - couleur) < abs(avp - couleur)):
        return 0

    return 1

def _minitel_arp(niveau):
    """Convertit un niveau en une séquence de codes Minitel définissant la
    couleur d’arrière-plan.

    :param niveau:
        Le niveau à convertir (valeur de 0 à 7 inclus).
    :type niveau:
        un entier

    :returns:
        Un objet de type Sequence contenant la séquence à envoyer au
        Minitel pour avec une couleur d’arrière-plan correspondant au
        niveau.
    """
    assert isinstance(niveau, int)

    try:
        return Sequence([ESC, 0x50 + COULEURS_MINITEL[niveau]])
    except IndexError:
        return Sequence([ESC, 0x50])

def _minitel_avp(niveau):
    """Convertit un niveau en une séquence de codes Minitel définissant la
    couleur d’avant-plan.

    :param niveau:
        Le niveau à convertir (valeur de 0 à 7 inclus).
    :type niveau:
        un entier

    :returns:
        Un objet de type Sequence contenant la séquence à envoyer au
        Minitel pour avec une couleur d’avant-plan correspondant au niveau.
    """
    assert isinstance(niveau, int)

    try:
        return Sequence([ESC, 0x40 + COULEURS_MINITEL[niveau]])
    except IndexError:
        return Sequence([ESC, 0x47])

class ImageMinitel:
    """Une classe de gestion d’images Minitel avec conversion depuis une image
    lisible par PIL.

    Cette classe gère une image au sens Minitel du terme, c’est à dire par
    l’utilisation du mode semi-graphique dans lequel un caractère contient
    une combinaison de 2×3 pixels. Cela donne une résolution maximale de 80×72
    pixels.
    
    Hormis la faible résolution ainsi obtenue, le mode semi-graphique présente
    plusieurs inconvénients par rapport à un véritable mode graphique :

    - il ne peut y avoir que 2 couleurs par bloc de 2×3 pixels,
    - les pixels ne sont pas carrés
    """

    def __init__(self, disjoint = False):
        """Constructeur

        :param disjoint:
            Active le mode disjoint pour les images.
        :type disjoint:
            un booléen
        """
        assert isinstance(disjoint, bool)

        # L’image est stockées sous forme de Sequences afin de pouvoir
        # l’afficher à n’importe quelle position sur l’écran
        self.sequences = []

        self.largeur = 0
        self.hauteur = 0
        self.disjoint = disjoint

    def envoyer(self, out, colonne = 1, ligne = 1):
        """Envoie l’image sur le Minitel à une position donnée

        Sur le Minitel, la première colonne a la valeur 1. La première ligne
        a également la valeur 1 bien que la ligne 0 existe. Cette dernière
        correspond à la ligne d’état et possède un fonctionnement différent
        des autres lignes.

        :param out:
            un objet sur lequel envoyer l'image
        
        :param colonne:
            colonne à laquelle positionner le coin haut gauche de l’image
        :type colonne:
            un entier

        :param ligne:
            ligne à laquelle positionner le coin haut gauche de l’image
        :type ligne:
            un entier
        """
        assert isinstance(colonne, int)
        assert isinstance(ligne, int)

        for sequence in self.sequences:
            out.pos(ligne, colonne)
            for v in sequence.valeurs:
                out._write(v.to_bytes(1, 'little'))
            ligne += 1

    def importer(self, image):
        """Importe une image de PIL et crée les séquences de code Minitel
        correspondantes. L’image fournie doit avoir été réduite à des
        dimensions inférieures ou égales à 80×72 pixels. La largeur doit être
        un multiple de 2 et la hauteur un multiple de 3.

        :param image:
            L’image à importer.
        :type niveau:
            une Image
        """
        assert image.size[0] <= 80
        assert image.size[1] <= 72

        # En mode semi-graphique, un caractère a 2 pixels de largeur
        # et 3 pixels de hauteur
        self.largeur = int(image.size[0] / 2)
        self.hauteur = int(image.size[1] / 3)

        # Initialise la liste des séquences
        self.sequences = []

        for hauteur in range(0, self.hauteur):
            # Variables pour l’optimisation du code généré
            old_arp = -1
            old_avp = -1
            old_alpha = 0
            compte = 0

            # Initialise une nouvelle séquence
            sequence = Sequence()

            # Passe en mode semi-graphique
            sequence.ajoute(SO)

            if self.disjoint:
                sequence.ajoute([ESC, 0x5A])

            for largeur in range(0, self.largeur):
                # Récupère 6 pixels
                pixels = [
                    image.getpixel((largeur * 2 + x, hauteur * 3 + y))
                    for x, y in [(0, 0), (1, 0),
                                  (0, 1), (1, 1),
                                  (0, 2), (1, 2)]
                ]

                if self.disjoint:
                    # Convertit chaque couleur de pixel en deux niveaux de gris
                    pixels = [_huit_niveaux(pixel) for pixel in pixels]

                    arp, avp = _deux_couleurs(pixels)

                    if arp != 0:
                        arp, avp = 0, arp

                else:
                    # Convertit chaque couleur de pixel en huit niveau de gris
                    pixels = [_huit_niveaux(pixel) for pixel in pixels]

                    # Recherche les deux couleurs les plus fréquentes
                    # un caractère ne peut avoir que deux couleurs !
                    arp, avp = _deux_couleurs(pixels)

                # Réduit à deux le nombre de couleurs dans un bloc de 6 pixels
                # Cela peut faire apparaître des artefacts mais est inévitable
                pixels = [_arp_ou_avp(pixel, arp, avp) for pixel in pixels]

                # Convertit les 6 pixels en un caractère mosaïque du minitel
                # Le caractère est codé sur 7 bits
                bits = [
                    '0',
                    str(pixels[5]),
                    '1',
                    str(pixels[4]),
                    str(pixels[3]),
                    str(pixels[2]),
                    str(pixels[1]),
                    str(pixels[0])
                ]

                # Génère l’octet (7 bits) du caractère mosaïque
                alpha = int(''.join(bits), 2)

                # Si les couleurs du précédent caractères sont inversés,
                # inverse le caractère mosaïque. Cela évite d’émettre
                # à nouveau des codes couleurs. Cela fonctionne uniquement
                # lorsque le mode disjoint n’est pas actif
                if not self.disjoint and old_arp == avp and old_avp == arp:
                    # Inverse chaque bit à l’exception du 6e et du 8e
                    alpha = alpha ^ 0b01011111
                    avp, arp = arp, avp
                    
                if old_arp == arp and old_avp == avp and alpha == old_alpha:
                    # Les précédents pixels sont identiques, on le retient
                    # pour utiliser un code de répétition plus tard
                    compte += 1
                else:
                    # Les pixels ont changé, mais il peut y avoir des pixels
                    # qui n’ont pas encore été émis pour cause d’optimisation
                    if compte > 0:
                        if compte == 1:
                            sequence.ajoute(old_alpha)
                        else:
                            sequence.ajoute([DC2, 0x40 + compte])

                        compte = 0

                    # Génère les codes Minitel
                    if old_arp != arp:
                        # L’arrière-plan a changé
                        sequence.ajoute(_minitel_arp(arp))
                        old_arp = arp

                    if old_avp != avp:
                        # L’avant-plan a changé
                        sequence.ajoute(_minitel_avp(avp))
                        old_avp = avp

                    sequence.ajoute(alpha)
                    old_alpha = alpha

            if compte > 0:
                if compte == 1:
                    sequence.ajoute(old_alpha)
                else:
                    sequence.ajoute([DC2, 0x40 + compte])

                compte = 0

            if self.disjoint:
                sequence.ajoute([ESC, 0x59])

            # Une ligne vient d’être terminée, on la stocke dans la liste des
            # séquences
            self.sequences.append(sequence)

"""Constants used by the Minitel protocol."""

import codecs
import string

special_chars = {
    'à': b'\x19\x41a',
    'â': b'\x19\x43a',
    'ä': b'\x19\x48a',
    'è': b'\x19\x41e',
    'é': b'\x19\x42e',
    'ê': b'\x19\x43e',
    'ë': b'\x19\x48e',
    'î': b'\x19\x43i',
    'ï': b'\x19\x48i',
    'ô': b'\x19\x43o',
    'ö': b'\x19\x48o',
    'ù': b'\x19\x43u',
    'û': b'\x19\x43u',
    'ü': b'\x19\x48u',
    'ç': b'\x19\x4Bc',
    '°': b'\x19\x30',
    '£': b'\x19\x23',
    'Œ': b'\x19\x6A',
    'œ': b'\x19\x7A',
    'ß': b'\x19\x7B',
    '¼': b'\x19\x3C',
    '½': b'\x19\x3D',
    '¾': b'\x19\x3E',
    '←': b'\x19\x2C',
    '↑': b'\x19\x2D',
    '→': b'\x19\x2E',
    '↓': b'\x19\x2F',
    '̶': b'\x60',
    '|': b'\x7C',
}

substitutions = {
    'À': b'A',
    'Â': b'A',
    'Ä': b'A',
    'È': b'E',
    'É': b'E',
    'Ê': b'E',
    'Ë': b'E',
    'Ï': b'I',
    'Î': b'I',
    'Ô': b'O',
    'Ö': b'O',
    'Ù': b'U',
    'Û': b'U',
    'Ü': b'U',
    'Ç': b'C',
    '’': b'\'',
    '•': b'*',
}

plain_ascii_substitutions = {
    'à': 'a',
    'â': 'a',
    'ä': 'a',
    'è': 'e',
    'é': 'e',
    'ê': 'e',
    'ë': 'e',
    'î': 'i',
    'ï': 'i',
    'ô': 'o',
    'ö': 'o',
    'ù': 'u',
    'û': 'u',
    'ü': 'u',
    'ç': 'c',
    '°': 'deg',
    '£': 'GBP',
    'Œ': 'OE',
    'œ': 'oe',
    'ß': 'ss',
    '¼': '1/4',
    '½': '1/2',
    '¾': '3/4',
    '←': '<-',
    '↑': '^',
    '→': '->',
    '↓': 'v',
    '̶': '[]',
    '|': '|',
    'À': 'A',
    'Â': 'A',
    'Ä': 'A',
    'È': 'E',
    'É': 'E',
    'Ê': 'E',
    'Ë': 'E',
    'Ï': 'I',
    'Î': 'I',
    'Ô': 'O',
    'Ö': 'O',
    'Ù': 'U',
    'Û': 'U',
    'Ü': 'U',
    'Ç': 'C',
    '’': '\'',
    '•': '*',
}

minitel_partial_encode_table = (
    {letter: bytes(letter, 'ascii') for letter in string.printable} |
    {ucode: byteval for ucode, byteval in special_chars.items()}
)

minitel_encode_table = (
    minitel_partial_encode_table |
    {ucode: byteval for ucode, byteval in substitutions.items()}
)

minitel_decode_table = (
    {int.from_bytes(v, "big"): k for k, v in minitel_partial_encode_table.items()}
)

def minitel_encode(text: str) -> tuple[bytes, int]:
    return b''.join(minitel_encode_table.get(chr(x) if type(x) is int else x, b' ') for x in text), len(text)

def minitel_decode(binary: bytes) -> tuple[str, int]:
    return ''.join(minitel_decode_table.get(x, ' ') for x in binary), len(binary)


def minitel_search_function(encoding_name):
    return codecs.CodecInfo(minitel_encode, minitel_decode, name='minitel')

codecs.register(minitel_search_function)

def abytes(str):
    """Handy shortcut to convert a string to minitel-compatible bytes."""
    return bytes(str, encoding='minitel')

# Control codes
SEP = b'\x13'
ESC = b'\x1b'
SOH = b'\x01'
EOT = b'\x04'
NUL = b'\x00'

# Termcaps
tHome = b'\x1e'
tMoveCursor = b'\x1f'
tLine = lambda l: abytes(chr(0x40+l))
tCol = lambda c: abytes(chr(0x40+c))
tBgColor = lambda c: ESC + abytes(chr(0x50+c))
tFgColor = lambda c: ESC+ abytes(chr(0x40+c))
tCursorOn = b'\x11'
tCursorOff = b'\x14'
tRepeatPrev = lambda count: b'\x12' + abytes(chr(0x40+count))
tBlinkOn = b'\x48'                    # H
tBlinkOff = b'\x73'                   # s
tVideoInverseStart = b'\x5d'          # ]
tVideoInverseEnd = b'\x5c'             # \
tVideoTransparent = b'\x5e'           # ^
tBell = b'\x07'
tClearScreen = b'\x0c'
tKeyboardLower = b'\x1b\x3a\x69\x45'  # \x1b:iE
tKeyboardUpper = b'\x1b\x3a\x6a\x45'  # \x1b:jE
tModePage = b'\x1b\x3a\x6a\x40'       # \x1b:j@
tPRO1 = b'\x39'                       # 9
tPRO2 = b'\x3a'                       # :
tPRO3 = b'\x3b'                       # ;
tENQROM = b'\x7b'                     # {
tVideotexToMixte = b'\x32\x7d'        # 2}
tMixteToVideotex = b'\x32\x7e'        # 2~
tSemiGraphicalMode = b'\x0e'
tTextMode = b'\x0f'
tMoveLeft = b'\x08'
tMoveRight = b'\x09'
tMoveDown = b'\x0a'
tMoveUp = b'\x0b'
tSetNormalHeight = b'\x4c'            # L
tSetDoubleHeight = b'\x4d'            # M
tSetDoubleWidth = b'\x4e'             # N
tSetDoubleSize = b'\x4f'              # O
tStartUnderline = b'\x5a'             # Z
tEndUnderline = b'\x59'               # Y


# Protocol specifiers
pModeMask = b'\x23'          # # Mode masquage ecran
pModeTransparent = b'\x25'   # % Mode transparent ecran
pModeEnd = b'\x2f'           # Fin de mode
pCursorRequest = b'\x61'     # a Requete position curseur
pPeripheralCommand = b'\x01' # Commande d'un peripherique

# Colors
clBlack = 0x0
clRed = 0x1
clGreen = 0x2
clYellow = 0x3
clBlue = 0x4
clMagenta = 0x5
clCyan = 0x6
clWhite = 0x7

# Minitel key codes
kEnvoi = b'\x41'         # A
kRetour = b'\x42'        # B
kRepetition = b'\x43'    # C
kGuide = b'\x44'         # D
kAnnulation = b'\x45'    # E
kSommaire = b'\x46'      # F
kCorrection = b'\x47'    # G
kSuite = b'\x48'         # H
kConnexionfin = b'\x49'  # I
kModemConnect = b'\x53'  # S

# Switch ("aiguillage") commands
swOFF = b'\x60'          # `
swON = b'\x61'           # a
swFromScreen = b'\x58'   # X
swFromKeyboard = b'\x59' # Y
swFromModem = b'\x5a'    # Z
swFromPort = b'\x5b'     # [
swFromPhone = b'\x5c'    # \
swFromSoftware = b'\x5d' # ^]
swToScreen = b'\x50'     # P
swToKeyboard = b'\x51'   # Q
swToModem = b'\x52'      # R
swToPort = b'\x53'       # S
swToPhone = b'\x54'      # T
swToSoftware = b'\x55'   # U

"""Constants used by the Minitel protocol."""

def abytes(str):
    """Handy shortcut to convert an ascrii string to bytes."""
    return bytes(str, encoding='ascii')

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

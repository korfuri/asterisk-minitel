# Termcaps
tHome = b'\x1e'
tMoveCursor = b'\x1f'
tLine = lambda l: abytes(chr(0x40+l))
tCol = lambda c: abytes(chr(0x40+c))
tBgColor = lambda c: abytes(chr(0x50+c))
tFgColor = lambda c: abytes(chr(0x40+c))
tCursorOn = b'\x11'
tCursorOff = b'\x14'
tBlinkOn = b'\x48'
tBlinkOff = b'\x73'
tBell = b'\x07'
tKeyboardLower = b'\x1b\x3a\x69\x45'
tKeyboardUpper = b'\x1b\x3a\x6a\x45'
tPRO1 = b'\x1b\x39'
tPRO2 = b'\x1b\x3a'
tPRO3 = b'\x1b\x3b'
tENQROM = b'\x7b'

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

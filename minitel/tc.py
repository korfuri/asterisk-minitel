from minitel.constants import *
import logging


class ConnectionError(Exception):
    """Generic exception type for connection errors. Subclass me."""
    pass


class ConnectionInterruptedError(ConnectionError):
    """Connection was interrupted, and reading/writing is impossible."""
    pass


class NotAllDataSentError(ConnectionError):
    """Not all data was successfully sent to the socket.

    TODO: if this actually happens, we should handle it gracefully and
    retry writing missing data (until successful or
    ConnectionInterruptederror). But it's HIGHLY unlikely we'll run
    into this.
    """
    pass


class UserDisconnected(ConnectionError):
    """User requested to disconnect, terminating the session."""
    pass


class ProtocolError(ConnectionError):
    """We couldn't make sense of a message we received."""


class Break:
    """A symbol for `stop handling input`.

    This is meant to be used as a keyHandler, to signify that input
    should not be processed further.
    Control is then returned to the application layer, for further
    dispatch or processing.
    """
    pass


class InputField:
    """Logic to handle an input field on a Minitel screen.

    An input field is a location at which the user is expected to
    enter text.

    Methods in this class don't access the Minitel socket directly,
    instead they return bytes to send to the Minitel socket. I/O
    remains the responsibility of the MinitelTerminal class.

    TODO: consider multi-line fields

    """
    def __init__(self, line, col, maxlength, contents, color = b''):
        self.line = line
        self.col = col
        self.maxlength = maxlength
        self.contents = contents
        assert(isinstance(color, bytes))
        self.color = color

    def display(self):
        return (tMoveCursor + tLine(self.line) + tCol(self.col) + self.color +
                (abytes('.') * self.maxlength) +
                tMoveCursor + tLine(self.line) + tCol(self.col) + self.color +
                abytes(self.contents)
                )

    def handleChar(self, c):
        """Handles a key event from the user."""
        if c == b'\n' or c == b'\r':
            return tBell
        if len(self.contents) + len(c) >= self.maxlength:
            return tBell
        self.contents = self.contents + c.decode('ascii')
        return c

    def correct(self):
        self.contents = self.contents[:-1]
        return self.display()

    def erase(self):
        self.contents = ""
        return self.display()


class MinitelTerminal:
    """A utility class handling a Minitel terminal screen.

    This provides functionalities for reading and writing to/from the
    terminal, including termcaps access, event handling and input
    field management.

    """

    def __init__(self, socket):
        self.socket = socket
        self.inputFields = []
        self.resetKeyHandlers()
        self.HandleCharacter = self.handleCharacterToTextInput
        self._lastControlKey = None

    #  ##############################################
    #  Connection management
    #  ##############################################

    def _write(self, data):
        """Send data to the underlying socket.

        Errors are handled by raising exceptions.

        TODO: handle retrying if only part of the data was written.

        """
        l = len(data)
        if l == 0:
            return
        logging.debug("send> %s", repr(data))
        sent = self.socket.send(data)
        if sent == 0:
            logging.debug("send failed, connection interrupted")
            raise ConnectionInterruptedError
        elif sent != l:
            logging.debug("send failed, not all data sent")
            raise NotAllDataSentError

    def _read(self, length):
        """Read data from the underlying socket.

        Errors are handled by raising exceptions.

        """
        r = self.socket.recv(length)
        if len(r) == 0:
            logging.debug("read failed, connection interrupted")
            raise ConnectionInterruptedError
        logging.debug("read< %s", repr(r))
        return r

    def _consume(self, length):
        """Read exactly this much data from the underlying socket.

        Unlinke _read, this will retry until enough bytes have been
        received.
        """
        data = bytes(0)
        while length > 0:
            r = self._read(length)
            data = data + r
            length = length - len(r)
        return data

    def start(self):
        """Handle the initital exchange with the Minitel.

        We wait for an UML header and a CxFin event, then immediately
        query the minitel's capabilities and store them.

        """
        # ignore the actual contents of the ULM header, they're irrelevant
        # we could take the transmission speed into consideration, but
        # it's so laughably slow in all scenarios that we just don't
        # care
        # ex = b'Version: 1\r\nTXspeed: 133.33\r\nRXspeed: 8.33\r\n\r\n\x13'
        # len(ex) == 47
        data = bytes(0)
        while True:
            data = data + self._read(200)

            # Wait for a Modem Connect event, which is sent
            # automatically as the user pressed CxFin.  If for any
            # reason this isn't received successfully, the user can
            # press Sommaire instead.
            logging.debug("Expecting: %s or %s", (SEP+kModemConnect), (SEP + kSommaire))
            logging.debug("data is: %s", data)
            if (SEP + kModemConnect) in data or (SEP + kSommaire) in data:
                logging.debug("breaking successfully")
                break
        self.query_capabilities()

    def print(self, text):
        """Display raw text."""
        self._write(abytes(text))

    def sendfile(self, path):
        """Send a file at indicated path to the Minitel.

        This is mainly useful to send serialized vtel layouts.

        """
        with open(path, 'rb') as f:
            self.socket.send(f.read())

    def disconnect(self):
        """Disconnect the socket.

        This can be used as a keyHandler for the kConnexionFin event.

        """
        self.socket.close()
        raise UserDisconnected

    #  ##############################################
    #  Termcap facilities and visual effects.
    #  See also termcap constants above in the file.
    #  ##############################################

    def pos(self, l, c=1):
        """Positions the cursor at given line and column."""
        if l == 1 and c == 1:
            self._write(tHome)
        else:
            self._write(tMoveCursor + tLine(l) + tCol(c))

    def query_capabilities(self):
        """Queries the capabilities of the Minitel.

        TODO: implement this properly.
        """
 
        self._write(ESC + tPRO1 + tENQROM)
        data = self._consume(5)
        # if len(data) != 5 or data[0] != SOH or data[4] != EOT:
        #     logging.error("data was: %s", data)
        #     raise ProtocolError()
        # self.terminfo = termInfos.get(data[2], "minitel")
        self.terminfo = "minitel1-nb"

    def clear(self):
        """Clears the screen and resets terminal state."""
        self.pos(0, 1)
        self._write(tClearScreen)
        self._write(tMoveCursor + tLine(0) + tCol(1) + b'\x18\x0a') # Go to home row, clear it
        self._write(tKeyboardUpper)

    def setMode(self, mode):
        self._write(ESC + tPRO2 + mode)

    def textBox(self, line, col, width, height, text, effects=b''):
        textwidth = width - 2
        for l in range(height):
            self.pos(line + l, col)
            self._write(effects)
            # Write a leading space, to pick up the bgcolor
            self.print(' ')
            text_this_line = text[:textwidth]
            text = text[textwidth:]
            padding = width - len(text_this_line) - 1
            self.print(text_this_line)
            if padding > 0:
                self._write(tSemiGraphicalMode)
                self.print(' ' * padding)
                # if padding < 3:
                #     self._write(b' ' * padding)
                # else:
                #     self._write(b' ' + tRepeatPrev(padding))
            
    def reset(self):
        """Resets all terminal state."""
        self.resetInputFields()
        self.resetKeyHandlers()
        self.setMode(tMixteToVideotex)
        self.clear()
        self.HandleCharacter = self.handleCharacterToTextInput

    #  ##############################################
    #  Input field management
    #  ##############################################

    def resetInputFields(self):
        """Drops all input fields."""
        self.inputFields = []
        self.activeInputField = None

    def addInputField(self, *args, **kwargs):
        """Creates a new input field.

        Parameters are passed direclty to the InputField class.
        The new input field becomes the active input field.

        """
        i = InputField(*args, **kwargs)
        self.inputFields.append(i)
        self.activeInputField = i
        self._write(i.display())
        return i

    def nextInputField(self):
        """Cycles active input field through the list.

        This is intended as a keyHandler for kSuite.
        """
        if self.activeInputField is None:
            return
        i = self.inputFields.index(self.activeInputField)
        self.activeInputField = (
            self.inputFields[(i + 1) % len(self.inputFields)])
        self._write(self.activeInputField.display())

    def correctInputField(self):
        if self.activeInputField is None:
            return
        self._write(self.activeInputField.correct())

    def eraseInputField(self):
        if self.activeInputField is None:
            return
        self._write(self.activeInputField.erase())

    #  ##############################################
    #  Key event handler management and input dispatch
    #  ##############################################

    def resetKeyHandlers(self):
        self.keyHandlers = {
            kConnexionfin: self.disconnect,
            kSuite: self.nextInputField,
            kCorrection: self.correctInputField,
            kAnnulation: self.eraseInputField,
            kSommaire: Break,
            kGuide: Break,
            kRepetition: Break,
            kRetour: Break,
        }

    def handleCharacterToTextInput(self, c):
        """Receive a character as input and dispatch it to the active
        input field.

        This is intended to be used as a receiver for self.HandleCharacter.
        """
        if self.activeInputField:
            r = self.activeInputField.handleChar(c)
            self._write(r)

    def handleInputsUntilBreak(self):
        while True:
            if self.handleNextInput() is Break:
                return

    def handleNextInput(self):
        c = self._read(1)
        if c == SEP:  # This is a minitel key
            c = self._read(1)
            if c in self.keyHandlers:
                self._lastControlKey = c
                if self.keyHandlers[c] is Break:
                    return Break
                else:
                    if self.keyHandlers[c]() is Break:
                        return Break
            else:
                logging.debug("No handler for key %s", c)
        elif c == ESC:  # Protocol acknowledgements
            self.handleAcknowledgement()
        else:
            self.HandleCharacter(c)

    def lastControlKey(self):
        return self._lastControlKey

    def handleAcknowledgement(self):

        """Called after a \x1B byte, indicating protocol control events.

        This function consumes the (variable length) message. Perhaps
        in the future we'll do something with the acknowledgements,
        for now we just drop them on the floor.

        The protocol codes can be found at:
        https://millevaches.hydraule.org/info/minitel/specs/codes.htm

        """
        c = self._read(1)
        if c == pModeMask:
            self._consume(2)  # Masquage/demasquage ecran
        elif c == pModeTransparent:
            pass
        elif c == pModeEnd:
            self._consume(1)
        elif c == pCursorRequest:
            pass
        elif c == pPeripheralCommand:        # Commande d'un peripherique
            self._consume(1)
        elif c == tPRO1:
            self._consume(1)
        elif c == tPRO2:
            self._consume(2)
        elif c == tPRO3:
            self._consume(3)
        else:
            log.error("Unknown protocol command %s, flushing read buffer", c)
            self._read(1000)

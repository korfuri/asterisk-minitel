import unittest

from minitel.tc import InputField
from minitel.constants import clWhite

class InputFieldTest(unittest.TestCase):
    def testEditLogic(self):
        i = InputField(1, 1, 10, "init", clWhite)
        i.handleChar(b'i')
        self.assertEqual(i.contents, "initi")
        i.correct()
        self.assertEqual(i.contents, "init")
        i.erase()
        self.assertEqual(i.contents, "")
        i.correct()
        self.assertEqual(i.contents, "")
        i.handleChar(b'a')
        self.assertEqual(i.contents, "a")

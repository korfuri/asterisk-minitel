import unittest

from minitel import InputField
from minitel.constants import clWhite

class InputFieldTest(unittest.TestCase):
    def testEditLogic(self):
        i = InputField(1, 1, 10, "init", clWhite)

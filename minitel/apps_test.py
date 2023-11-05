import unittest
from unittest.mock import MagicMock
import minitel.apps
import minitel.minitelhandler
import minitel.tc
import minitel.database
from absl.testing import absltest


class FakeSocket(object):
    def __init__(self, toReceive=bytes()):
        self.sent = bytes()
        self.toReceive = toReceive

    def send(self, data):
        self.sent = self.sent + data
        return len(data)

    def recv(self, length):
        r = self.toReceive[:length]
        self.toReceive = self.toReceive[length:]
        return r

class AppsCanInteractTest(absltest.TestCase):
    def setUp(self):
        # Apps that rely on the database need it to be setup first.
        # `sqlite://` is an in-memory database path.
        engine = minitel.database.GetEngine(db_path='sqlite://')
        minitel.database.Migrate()

    def testInteract(self):
        for name, appclass in minitel.apps.apps_directory.items():
            with self.subTest(app=name):
                socket = FakeSocket(minitel.tc.SEP + minitel.tc.kModemConnect)
                m = minitel.tc.MinitelTerminal(socket)
                m.start()
                # Pretend the user hit the Sommaire key immediately
                socket.toReceive = (minitel.tc.SEP + minitel.tc.kSommaire)
                m.reset()
                app = appclass(m)
                app.begin()
                app.interact()

if __name__ == '__main__':
    absltest.main()

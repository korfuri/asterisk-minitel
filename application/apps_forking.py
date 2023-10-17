import tc
from apps import ForkingApp, register

@register("nethack")
class NethackApp(ForkingApp):
    def interact(self):
        self.m._write(tKeyboardLower)
        self.spawn(["nethack"])

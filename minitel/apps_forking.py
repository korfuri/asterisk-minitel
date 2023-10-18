import minitel.tc as tc
from minitel.apps import ForkingApp, register


@register("nethack")
class NethackApp(ForkingApp):
    def interact(self):
        self.m._write(tc.tKeyboardLower)
        self.spawn("nethack")


@register("demo", ["cacademo", "caca"])
class DemokApp(ForkingApp):
    def interact(self):
        self.spawn("cacademo")


@register("env")
class EnvApp(ForkingApp):
    def interact(self):
        self.spawn("env")
        self.m.handleInputsUntilBreak()


@register("clock")
class ClockApp(ForkingApp):
    def interact(self):
        self.spawn("watch -n 1 date")

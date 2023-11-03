import minitel.tc as tc
from minitel.apps import ForkingApp, register, BaseApp
import minitel.constants as constants
from absl import flags


flags.DEFINE_bool("debug_apps", False, "Enable debug-only apps that may be dangerous when publicly available")


ENV_MIXTE = {
    # Environment for a Mixte mode terminal
    "TERM": "vt100",
    "COLUMNS": "80",
    "LINES": "25",
}


# @register("nethack")
# class NethackApp(ForkingApp):
#     def interact(self):
#         self.m.setMode(constants.tVideotexToMixte)
#         self.spawn("nethack", env=ENV_MIXTE)


# @register("clock")
# class ClockApp(ForkingApp):
#     def interact(self):
#         self.spawn("watch -n 1 date")


# @register("web")
# class BrowserApp(ForkingApp):
#     def interact(self):
#         if not flags.FLAGS.debug_apps:
#             return
#         self.m.setMode(constants.tVideotexToMixte)
#         self.spawn("lynx", env=ENV_MIXTE)


# @register("sh")
# class ShellApp(ForkingApp):
#     def interact(self):
#         if not flags.FLAGS.debug_apps:
#             return
#         self.m.setMode(constants.tVideotexToMixte)
#         self.spawn("sh", env=ENV_MIXTE)

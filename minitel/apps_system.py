from minitel.apps import BaseApp, register
from minitel.assets import asset

@register("sys/error")
class ErrorApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("CRITICAL_ERROR.vdt"))
        self.m.handleInputsUntilBreak()

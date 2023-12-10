from minitel.apps import BaseApp, register
from minitel.assets import asset
import minitel.tc as tc
from PIL import Image
import logging
import os

@register("sys/error")
class ErrorApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("CRITICAL_ERROR.vdt"))
        self.m.handleInputsUntilBreak()

from minitel.ImageMinitel import ImageMinitel

@register("a")
class DemoApp(BaseApp):
    def interact(self):
        imgs = os.listdir(asset("q2"))
        for i in imgs:
            self.m.reset()
            image = Image.open(asset("q2/" + i))
            image.thumbnail((80, 72), Image.LANCZOS)
            logging.info("Image size: %s %s" % (image.size[0], image.size[1]))
            image_minitel = ImageMinitel()
            image_minitel.importer(image)
            image_minitel.envoyer(self.m, 1, 1)
            im = ImageMinitel()
            self.m.keyHandlers[tc.kSuite] = tc.Break
            self.m.handleInputsUntilBreak()

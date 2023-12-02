from minitel.apps import BaseApp, register
from minitel.assets import asset
from PIL import Image

@register("sys/error")
class ErrorApp(BaseApp):
    def interact(self):
        self.m.sendfile(asset("CRITICAL_ERROR.vdt"))
        self.m.handleInputsUntilBreak()

from minitel.ImageMinitel import ImageMinitel
        
@register("sys/image")
class ErrorApp(BaseApp):
    def interact(self):
        largeur, hauteur, colonne, ligne = 60, 60, 1, 1
        image = Image.open(asset("fraise.jpg"))
        image = image.resize((largeur, hauteur), Image.LANCZOS)
        
        image_minitel = ImageMinitel()
        image_minitel.importer(image)
        image_minitel.envoyer(self.m, colonne, ligne)
        
        im = ImageMinitel()
        
        self.m.handleInputsUntilBreak()

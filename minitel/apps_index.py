import logging
import minitel.tc as tc
from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset

# @register("3615")
class Index3615App(BaseApp):
    def interact(self):
        global apps_directory
        self.m.sendfile(asset("3615.vdt"))
        code = self.m.addInputField(4, 9, 12, "")
        self.m.keyHandlers[tc.kEnvoi] = tc.Break
        self.m.handleInputsUntilBreak()
        logging.debug("Code: %s", code.contents)
        self.nextApp = appForCode(code.contents)

guide_directory = {
    # Max length: ------------------------------|xxxx
    'CONSENTEMENT': 'Commencez par ici',
    'ELECTIONS': 'Resultats des elections',
    'GISCORP': 'Entreprise innovante',
    'ASTRO': 'Votre futur est dans les etoiles',
    'ANNONCES': 'Faites de belles rencontres et ',
    'FERN': 'La recherche fondamentale',
    # menus
    # lineup
    # ateliers
    # aide
    
}

@register("guide")
class GuideApp(BaseApp):
    def interact(self):
        global guide_directory
        self.m.sendfile(asset("GUIDE.vdt"))
        for i, (name, desc) in enumerate(guide_directory.items()):
            self.m.pos(7+i, 1)
            self.m.setInverse()
            self.m.print(name)
            self.m.setNotInverse()
            self.m.print(" %s\r\n " % desc[:(39-len(name))])
        self.m.handleInputsUntilBreak()

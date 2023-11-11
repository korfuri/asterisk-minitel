import logging
import minitel.tc as tc
from minitel.apps import BaseApp, register
from minitel.assets import asset

@register("3615")
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
    'ELECTIONS': 'Résultats des élections nationales',
    'GISCORP': 'Informations et services de la GISCORP',
    'ASTRO': 'Votre futur est dans les étoiles',
    'ANNONCES': 'Faites la rencontre de votre vie, ou de votre nuit',
    # regles
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
        self.m.pos(7, 3)
        for name, desc in guide_directory.items():
            self.m.print(name)
            self.m.print('\r\n  ')
        self.m.handleInputsUntilBreak()

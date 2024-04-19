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
    'INFOS': 'L\'info en continu',
    'METEO': 'Informations meteorologiques',
    'ELECTIONS': 'Resultats des elections',
    'GISCORP': 'Entreprise innovante',
    # 'ANNONCES': 'Achetez, vendez, donnez',
    'ASTRO': 'Votre futur est dans les etoiles',
    'CHAT': 'Discute en direct avec des gens de ta région',
    # 'TROMBINET': 'Le réseau social de la Minitel Economy',
    #    'ULLA': 'Faites de belles rencontres !',
    #    'TF1': 'Premiere chaine d\'info nationale',
    # 'FERN': 'La recherche fondamentale',
    #    'MEETIC': 'L\'amour de votre vie, ici',
    #    'FSTX': 'Le seminaire de la GISCORP',
    'LINEUP': 'Du gros SON tout le weekend',
    'ATELIERS': 'Mentes sanae in corporibus sanis',
    'ARCHIVE': 'Toute la sagesse des anciens',
    'WANTED': 'Avis de recherche des disparus',
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

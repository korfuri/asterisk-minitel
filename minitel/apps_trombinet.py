from minitel.apps import BaseApp, register
from minitel.assets import asset
from minitel.ImageMinitel import ImageMinitel
import minitel.tc as tc
from PIL import Image
import json
import logging
import os
import pathlib
import random


@register("trombinet", ["facebook", "linkedin", "google+"])
class FacebookApp(BaseApp):
    def interact(self):
        self.m.reset()
        self.m.sendfile(asset("trombinet/trombinet.vdt"))

        is_image = random.choice([True, False, False, False])
        if is_image:
            imgs = os.listdir(asset("trombinet/pics"))
            i = random.choice(imgs)
            image = Image.open(asset("trombinet/pics/" + i))
            image.thumbnail((80, 60), Image.LANCZOS)
            image_minitel = ImageMinitel()
            image_minitel.importer(image)
            self.m.pos(1, 1)
            self.m.setTextMode()
            tags = pathlib.Path(i).stem.split('_')
            self.m.print((' '.join([' #%s' % t for t in tags])).strip(' '))
            image_minitel.envoyer(self.m, 1, 2)
        else:
            status = self.get_status()
            self.m.textBox(2, 1, 40, 20, status)

        self.m.pos(23, 1)
        self.m.setTextMode()
        self.m.print(self.get_poster())
        def repeat():
            self.nextApp = FacebookApp
            return tc.Break
        self.m.keyHandlers[tc.kSuite] = repeat
        self.m.pos(23, 32)
        self.m.print(self.get_likes())  # TODO
        self.m.handleInputsUntilBreak()

    def get_poster(self):
        first = random.choice([
            'Nicolas',
            'Julien',
            'Aurélie',
            'Sébastien',
            'Céline',
            'Emilie',
            'David',
            'Laëtitia',
            'Cédric',
            'Guillaume',
            'Elodie',
            'Stéphanie',
            'Virginie',
            'Audrey',
            'Jérôme',
            'Marie',
            'Alexandre',
            'Julie',
            'Christophe',
            'Vincent',
            'Sabrina',
            'Frédéric',
            'Sophie',
            'Thomas',
            'Vanessa',
            'Mathieu',
            'Grégory',
            'Caroline',
            'Olivier',
            'Romain',
            'Mickael',
            'Ludovic',
            'Stéphane',
            'Jessica',
            'Anthony',
            'Delphine',
            'Mélanie',
            'Angélique',
            'Sandrine',
            'Sylvain',
            'Damien',
            'Arnaud',
            'Laurent',
            'Nathalie',
            'Pierre',
            'Fabien',
            'Jonathan',
            'Benoit',
            'Benjamin',
            'Jérémy',
        ])
        return '@%s' % first

    def get_likes(self):
        return '%02d' % random.randrange(0, 99)

    def get_status(self):
        basedir = "trombinet/statuses"
        statusfiles = os.listdir(asset(basedir))
        with open(asset(basedir + "/" + random.choice(statusfiles))) as f:
            j = json.load(f)
            t = random.choice(j['choices'])['text']
            t = t.strip(" \"\n")
            return t

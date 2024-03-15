from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
import minitel.tc as tc
from absl import flags
from minitel.database import GetEngine, WantedPosting
import os
import logging
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from minitel.ImageMinitel import ImageMinitel
from PIL import Image, ExifTags
from willow.plugins.pillow import PillowImage

@register("wanted")
class WantedApp(BaseApp):
    def show_pic(self, path, x, y):
        image = Image.open(path)
        image.thumbnail((40, 60), Image.LANCZOS)
        image_minitel = ImageMinitel()
        image_minitel.importer(image)
        image_minitel.envoyer(self.m, x, y)

    def interact(self):
        self.m.sendfile(asset("fesste/avisderecherche.vdt"))

        with Session(GetEngine()) as session:
            wp = session.scalars(select(WantedPosting).order_by(func.random())).first()
        
        self.m.pos(3, 22)
        self.m.print(wp.name)

        self.m.pos(6, 22)
        self.m.setBlink()
        self.m.print(wp.statut)

        self.m.pos(9, 22)
        self.m.print(wp.contact)

        self.m.textBox(12, 22, 19, 4, wp.instructions)

        try:
            self.show_pic(os.path.join(flags.FLAGS.upload_path, wp.image), 1, 2)
        except Exception as e:
            logging.error(e)
        self.m.handleInputsUntilBreak()

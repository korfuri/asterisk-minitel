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
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif = image._getexif()
        if exif[orientation] == 3:
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image=image.rotate(90, expand=True)
        wimage = PillowImage(image)
        faces = wimage.detect_faces()
        if len(faces) > 0:
            box = faces[0]
            width = box[2] - box[0]
            height = box[3] - box[1]
            imgw, imgh = image.size
            ratio = 0.2
            box = (
                max(0, box[0] - ratio * width),
                max(0, box[1] - ratio * height),
                min(imgw, box[2] + ratio * width),
                min(imgh, box[3] + ratio * height),
            )
            image = image.crop(box)
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

from minitel.apps import BaseApp, register, appForCode
from minitel.assets import asset
import minitel.tc as tc
from minitel.database import GetEngine
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

        self.m.pos(3, 22)
        self.m.print("Uriel C.")

        self.m.pos(6, 22)
        self.m.setBlink()
        self.m.print("Disparu.e")

        self.m.pos(9, 22)
        self.m.print("Sedna")

        self.m.textBox(12, 22, 19, 4, "Lorem ipsum dolor sit amet consequetur adiscliptit elis. Unna bolerum tapioca magicien bellum. Sirti look at the sky it's turning red.")

        self.show_pic(asset("gallery/IMG_20240314_121042_815.jpg"), 1, 2)
        self.m.handleInputsUntilBreak()

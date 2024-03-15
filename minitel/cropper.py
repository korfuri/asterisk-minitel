from PIL import Image, ExifTags
from willow.plugins.pillow import PillowImage
from flask_admin.form.upload import ImageUploadField

class FaceImageUploadField(ImageUploadField):
    def __init__(self, *args, **kwargs):
        super(FaceImageUploadField, self).__init__(*args, **kwargs)
        # Set max_size to anything truthy, which will cause _resize to
        # be called. We'll be able to do our face detection and
        # cropping there.
        self.max_size = 1

    def _resize(self, image, size):
        """Override to crop to the first face found by openCV before
        resizing."""
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
            self.image = image.crop(box)
        return super(FaceImageUploadField, self)._resize(self.image, (40, 60, False,))

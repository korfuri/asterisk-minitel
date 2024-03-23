#!/usr/bin/env python3
import minitel.database as db
from absl import flags, app
from flask import Flask, send_from_directory, redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_admin.form.fields import Select2Field
from sqlalchemy.orm import Session
import logging
from minitel.assets import asset
import waitress
import random
import secrets
import string
from flask_admin.contrib.fileadmin import FileAdmin
from minitel.cropper import FaceImageUploadField


flags.DEFINE_string("upload_path", None, "Directory to upload user-generated content to")


def setup_admin(webapp):
    admin = Admin(webapp, name='maxitel', template_mode='bootstrap3')
    engine = db.GetEngine()
    session = Session(engine)
    admin.add_view(ModelView(db.Classified, session))
    admin.add_view(ModelView(db.QuestEntry, session))
    admin.add_view(ModelView(db.ChatMessage, session))
    admin.add_view(ModelView(db.WikiArticle, session))

    class WantedModelView(ModelView):
        form_overrides = {
            "image": FaceImageUploadField,
            "statut": Select2Field,
        }
        form_args = {
            "image": {
                "base_path": flags.FLAGS.upload_path,
                "url_relative_path": "uploads/",
                "namegen": lambda _o, _f: ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '.jpg'
            },
            "statut": {
                "choices": [
                    ("Vivant.e","Vivant.e",),
                    ("Disparu.e","Disparu.e",),
                    ("Zombifié.e","Zombifié.e",),
                    ("???","???",),
                    ("Mort.e","Mort.e",),
                    ("Ressucité.e","Ressucité.e",),
                ]
            },
        }

    admin.add_view(WantedModelView(db.WantedPosting, session))
    path = flags.FLAGS.upload_path
    admin.add_view(FileAdmin(path, '/static/', name='Uploaded Files'))


def startWebServer(*listener):
    webapp = Flask("maxitel")
    webapp.secret_key = secrets.token_hex()  # we don't care about persisting cookies across restarts
    webapp.config['SESSION_TYPE'] = 'filesystem'
    webapp.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    setup_admin(webapp)

    from flask import send_from_directory
    @webapp.route('/static/uploads/<path:path>')
    def uploads(path):
        return send_from_directory(flags.FLAGS.upload_path, path)

    @webapp.route('/e/<path:path>')
    def emulator(path):
        return send_from_directory(asset('emulator'), path)

    @webapp.route('/ws')
    def redirect_ws(path):
        return redirect("http://localhost:%d/" % flags.FLAGS.ws_port, code=302)

    logging.info("Web server listening on http://%s:%s", *listener)
    waitress.serve(webapp, listen='%s:%s' % listener)


def main(argv):
    db.Migrate()
    startWebServer()


if __name__ == '__main__':
    app.run(main)

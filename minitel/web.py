#!/usr/bin/env python3
import minitel.database as db
from absl import flags, app
from flask import Flask, send_from_directory
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import Session
import logging
from minitel.assets import asset


def setup_admin(webapp):
    admin = Admin(webapp, name='maxitel', template_mode='bootstrap3')
    engine = db.GetEngine()
    session = Session(engine)
    admin.add_view(ModelView(db.Classified, session))
    admin.add_view(ModelView(db.QuestEntry, session))

def startWebServer(*listener):
    webapp = Flask("maxitel")
    webapp.secret_key = 'super secret key'
    webapp.config['SESSION_TYPE'] = 'filesystem'
    webapp.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    # setup_admin(webapp)

    @webapp.route('/e/<path:path>')
    def send_report(path):
        return send_from_directory(asset('emulator'), path)

    logging.info("Web server listening on http://%s:%s", *listener)
    webapp.run(*listener)

def main(argv):
    db.Migrate()
    startWebServer()


if __name__ == '__main__':
    app.run(main)

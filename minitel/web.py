#!/usr/bin/env python3
import minitel.database as db
from absl import flags, app
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import Session

def runWebserver():
    webapp = Flask("maxitel")
    webapp.secret_key = 'super secret key'
    webapp.config['SESSION_TYPE'] = 'filesystem'
    webapp.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(webapp, name='maxitel', template_mode='bootstrap3')
    engine = db.GetEngine()
    session = Session(engine)
    admin.add_view(ModelView(db.Classified, session))
    admin.add_view(ModelView(db.QuestEntry, session))
    webapp.run()

def main(argv):
    db.Migrate()
    runWebserver()


if __name__ == '__main__':
    app.run(main)

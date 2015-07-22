import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore

app = Flask(__name__)
app.config.from_object('config')
heroku = Heroku(app)
db = SQLAlchemy(app)

from shabus.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

import shabus.views

if __name__ == '__main__':
    app.run(debug=True)

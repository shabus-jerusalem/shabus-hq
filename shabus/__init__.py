import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_bootstrap import Bootstrap
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object("config")
heroku = Heroku(app)
db = SQLAlchemy(app)
Bootstrap(app)
mail = Mail(app)


from shabus.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from shabus.admin import admin
import shabus.views

if __name__ == '__main__':
    app.run(debug=True)

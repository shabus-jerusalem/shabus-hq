import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object("config")
heroku = Heroku(app)
db = SQLAlchemy(app)
Bootstrap(app)

from shabus.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from shabus.admin import ProtectedModelView, ProtectedAdminIndexView
from shabus.models import Member, Passenger, Ride, Address
admin = Admin(app, name="shabus", template_mode="bootstrap3", index_view=ProtectedAdminIndexView())
admin.add_view(ProtectedModelView(Role, db.session))
admin.add_view(ProtectedModelView(User, db.session))
admin.add_view(ProtectedModelView(Member, db.session))
admin.add_view(ProtectedModelView(Passenger, db.session))
admin.add_view(ProtectedModelView(Ride, db.session))
admin.add_view(ProtectedModelView(Address, db.session))

import shabus.views

if __name__ == '__main__':
    app.run(debug=True)

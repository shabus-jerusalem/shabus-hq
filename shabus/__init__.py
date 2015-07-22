import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required


app = Flask(__name__)
heroku = Heroku(app)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config['DEBUG'] = True

#app.config['SECURITY_PASSWORD_HASH'] = "bcrypt"
#app.config['SECURITY_PASSWORD_SALT'] = "change this to something else"

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/')
@login_required
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
@login_required
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/robots.txt')
def send_text_file():
    """Send your static text file."""
    return app.send_static_file("robots.txt")

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

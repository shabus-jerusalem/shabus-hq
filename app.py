import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.heroku import Heroku
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask.ext.login import current_user, login_user, LoginManager, logout_user, login_required, UserMixin

app = Flask(__name__)
heroku = Heroku(app)
db = SQLAlchemy(app)
oid = OpenID(app, 'openid_store', safe_roots=[]) # TODO: modify path?
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(254), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=["email"])

    return render_template('login.html', form=form, providers=app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        flash('You are not allowed to log in. Please try again.')
        return redirect(url_for('login'))
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    next = request.args.get('next')
    if not next_is_valid(next):
        return flask.abort(400)

    return redirect(next or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

###
# Routing for your application.
###
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


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

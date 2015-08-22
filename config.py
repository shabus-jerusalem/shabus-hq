import os

DEBUG = True

SECRET_KEY = os.environ["FLASK_SECRET_KEY"]

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ["MAIL_USERNAME"]
MAIL_PASSWORD = os.environ["MAIL_PASSWORD"]

# CSRF_ENABLED = True
# CSRF_SESSION_KEY = "somethingimpossibletoguess"

# SECURITY_PASSWORD_HASH = "bcrypt" # TODO: is this right?
# SECURITY_PASSWORD_SALT = "change this to something else"

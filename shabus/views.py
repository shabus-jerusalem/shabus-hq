from flask import render_template, jsonify
from shabus import app
from flask.ext.security import login_required

@app.route('/')
@login_required
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/driver/', methods=['GET'])
@login_required
def driver():
    return render_template('driver.html')

@app.route('/driver/validate', methods=['POST'])
@login_required
def validate():
	# TODO: return approved false when needed
    return jsonify(status="OK", data=[{"text" : "User TEST was approved", "approved" : True}])

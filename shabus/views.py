# -*- coding: utf8 -*-
from flask import render_template, jsonify, request
from shabus import app, models
from flask.ext.security import login_required
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

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

@app.route('/driver/approve', methods=['POST'])
@login_required
def approve_ride():
    # TODO: return approved false when needed
    credentials = request.data
    query = models.Passenger.query.filter(or_(models.Passenger.phone_number==credentials,
                                                 models.Passenger.id_number==credentials))
    try:
    	passanger = query.one()
    	return jsonify(status="OK", data={"text" : "הנוסע/ת בשם {0} {1} מאושר. נסיעה טובה!".format(passanger.first_name, passanger.last_name), 
    									   "approved" : True})
    except sqlalchemy.orm.exc.NoResultFound:
    	return jsonify(status="ERROR", data={"text" : "לא זיהינו את הנוסע/ת {0}".format(credentials), "approved" : False})
    except sqlalchemy.orm.exc.MultipleResultsFound:
    	return jsonify(status="ERROR", data={"text" : "תקלה: ניתן לזהות יותר מנוסע אחד לפי {0}".format(credentials), "approved" : False})
    

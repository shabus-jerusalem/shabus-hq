# -*- coding: utf8 -*-
from flask import render_template, jsonify, request
from shabus import app, models, db
from flask.ext.security import login_required, core
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import json
import datetime

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
    # TODO: accept only unicode
    data = json.loads(request.data)
    print repr(data["id"])
    credentials = data["id"]
    position = data["position"]
    query = models.Passenger.query.filter(or_(models.Passenger.phone_number==credentials,
                                             models.Passenger.id_number==credentials))
    try:
        passanger = query.one()
        ride = models.Ride(
        	passenger_id = passanger.id,
        	board_time = datetime.datetime.now(),
        	recorded_by_user = core.current_user,
        	board_location = json.dumps(position)
        )
        db.session.add(ride)
        db.session.commit()
        return jsonify(status="OK", data={"text" : u"הנוסע/ת בשם {0} {1} מאושר. נסיעה טובה!".format(passanger.first_name, passanger.last_name), 
                                           "approved" : True})
    except NoResultFound:
        return jsonify(status="ERROR", data={"text" : u"לא זיהינו את הנוסע/ת {0}".format(credentials), "approved" : False})
    except MultipleResultsFound:
        return jsonify(status="ERROR", data={"text" : u"תקלה: ניתן לזהות יותר מנוסע אחד לפי {0}".format(credentials), "approved" : False})
    

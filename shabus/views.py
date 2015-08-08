# -*- coding: utf8 -*-
from flask import render_template, jsonify, request
from shabus import app, models, db, mail
from flask.ext.security import login_required, core
from flask_mail import Message
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import json
import datetime
import jotform
import import_members
import logging
import os
import traceback

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


@app.route('/signup', methods=['POST'])
def jotform_signup():
    # Security: make sure the user actually paid.
    if not jotform.validate_signup(request.form):
        return ""

    submission_id = request.form["submissionID"]
    logging.info("Got JotForm submission: %s" % submission_id)

    try:
        member_dict = jotform.get_member_dict(request.form)
        member, recommending_member_phone = import_members.add_member(member_dict)
        recommending_member_success = import_members.process_recommending_member_phone(
            member, recommending_member_phone)
        db.session.commit()
        if not recommending_member_success:
            send_error_email("Invalid recommending member.", submission_id)
    except:
        db.session.rollback()
        logging.exception("Error while processing submission:")
        send_error_email("Exception while processing submission:\n" + traceback.format_exc(), submission_id)

    logging.info("Submission processing finished")

    return ""

def send_error_email(error, submission_id):
    submission_link = jotform.JOTFORM_SUBMISSION_LINK % submission_id
    body = "Error while processing jotform submission with id %s.\nSubmittion details: %s\n\n%s" % (
        submission_id, submission_link, error)
    msg = Message(
        body=body,
        subject="Shabus JotForm Webhook Error",
        sender=("Shabus JotForm Webhook", "webhook@shabus.co.il"),
        recipients=os.environ["WEBHOOK_ERROR_RECIPIENTS"].split(";"))
    mail.send(msg)

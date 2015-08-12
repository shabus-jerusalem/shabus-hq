# -*- coding: utf8 -*-
from flask import render_template, jsonify, request
from shabus import app, models, db, mail
from flask.ext.security import login_required, core
from flask_mail import Message
from sqlalchemy import or_, desc
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
    credentials = data["id"]
    position = data["position"]
    query = models.Passenger.query.filter(or_(models.Passenger.phone_number==credentials,
                                             models.Passenger.id_number==credentials))
    try:
        passenger = query.one()
    except NoResultFound:
        return jsonify(
            status="ERROR",
            data={
                "text": u"לא זיהינו את הנוסע/ת {0}".format(credentials),
                "approved": False})
    except MultipleResultsFound:
        return jsonify(
            status="ERROR",
            data={
                "text": u"תקלה: ניתן לזהות יותר מנוסע אחד לפי {0}".format(credentials),
                "approved": False})

    query = models.Ride.query.filter(models.Ride.passenger_id == passenger.id).order_by(
        desc(models.Ride.board_time))
    last_ride = query.first()

    if last_ride and datetime.datetime.now() - last_ride.board_time < datetime.timedelta(minutes=5):
        return jsonify(
            status="OK",
            data={
                "text": (u"הנוסע/ת %s מאושר.<br />הנסיעה לא נרשמה " +
                    u"כיוון שלנוסע/ת כבר נרשמה נסיעה בחמש הדקות האחרונות.") % credentials,
                "approved": True})

    ride = models.Ride(
        passenger_id = passenger.id,
        board_time = datetime.datetime.now(),
        recorded_by_user = core.current_user,
        board_location = json.dumps(position)
    )
    db.session.add(ride)
    db.session.commit()
    if passenger.first_name is not None and passenger.last_name is not None:
        text = u"הנוסע/ת {0} {1} מאושר/ת.<br />".format(passenger.first_name, passenger.last_name)
    else:
        text = u"הנוסע/ת %s מאושר/ת.<br />" % credentials
    if passenger.passenger_type != "member":
        text += u"נסיעה נרשמה לחבר/ה %s.<br />" % passenger.member.email
    text += u"נסיעה טובה!"
    return jsonify(status="OK", data={"text" : text, "approved" : True})


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
        send_error_email(
            "Exception while processing submission:\n" + traceback.format_exc(),
            submission_id)

    logging.info("Submission processing finished")

    return ""

def send_error_email(error, submission_id):
    submission_link = jotform.JOTFORM_SUBMISSION_LINK % submission_id
    body = "Error while processing jotform submission with id %s.\nSubmittion details: %s\n\n%s" % (
        submission_id, submission_link, error)
    msg = Message(
        body=body,
        subject="Shabus JotForm Webhook Error",
        sender=os.environ["MAIL_SENDER"],
        recipients=os.environ["WEBHOOK_ERROR_RECIPIENTS"].split(";"))
    mail.send(msg)

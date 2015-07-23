from flask import render_template, jsonify
from shabus import app
from flask.ext.security import login_required
import jotform
import hopon

@app.route('/')
@login_required
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

############# DRIVER ########################################

@app.route('/driver/', methods=['GET'])
def driver():
    return render_template('driver.html')

############# AJAX CALLS FOR THE DRIVER PLATFORM #############

@app.route('/driver/login', methods=['POST'])
def login():
	# TODO: do the login
    return jsonify(status="OK", data=[{"text" : "Done"}])

@app.route('/driver/logout', methods=['POST'])
@login_required
def logout():
    # TODO: do the log out
    return jsonify(status="OK", data=[{"text" : "Done"}])

@app.route('/driver/validate', methods=['POST'])
@login_required
def validate():
	# TODO: return approved false when needed
    return jsonify(status="OK", data=[{"text" : "User TEST was approved", "approved" : True}])


########### WEBHOOK ##########################################

@app.route('/webhook/', methods=['POST'])
def webhook_process():
    submission_id = request.form["submissionID"]
    formResult = json.loads(request.form["rawRequest"])
    formResult = jotform.rename_fields(formResult)
    log_form(submission_id, formResult)
    if "mail" not in formResult:
        abort(400)

    hopOnResults = {}
    # Check if the user paid or has email / phone in headstart
    if hooks.validate_registration(formResult):
        # add the user to hopon
        app.logger.debug("[%s] User is valid.", submission_id)
        hopOnResults[formResult["phone"]] = hopon.create_shabus_user(formResult["phone"], "972")
        # Add the spouse if exists
        if formResult.get("spouse_phone"):
            app.logger.debug("[%s] User has spouse.", submission_id)
            hopOnResults[formResult["spouse_phone"]] = hopon.create_shabus_user(formResult["spouse_phone"], "972")
        # Add the children if exists
        if formResult.get("children_phone"):
            app.logger.debug("[%s] User has %d children.", submission_id,
                            formResult["children_phone"].count("\r\n") + 1)
            for phone in formResult["children_phone"].split("\r\n"):
                hopOnResults[phone] = hopon.create_shabus_user(phone, "972")

        for phone, result in hopOnResults.items():
            app.logger.debug("[%s] HoponResults[%s]: %r", submission_id, phone, result)

    # TODO: validate the hopOnResults
    # TODO: here come the db_part

    return "Success"




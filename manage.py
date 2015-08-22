from flask.ext.script import Manager
from flask_mail import Message
from shabus import app, db, mail
from shabus.models import Member
import os

manager = Manager(app)

@manager.command
def send_test_mail():
    message = Message(
        body="It worked!",
        subject="Shabus Test Email",
        sender=os.environ["MAIL_SENDER"],
        recipients=[raw_input("Recipient email address: ")])
    mail.send(message)

ADDRESS_ATTRIBUTES = ("address", "additional_address", "desired_destination_address")

@manager.command
def delete_members():
    member_ids_to_delete = raw_input("Member ids to delete, separated by commas:").split(",")
    deleted_passengers = deleted_addresses = 0
    for member_id in member_ids_to_delete:
        member = Member.get(member_id)
        for address_attribute in ADDRESS_ATTRIBUTES:
            if getattr(member, address_attribute) is not None:
                db.session.delete(getattr(member, additonal_address))
                setattr(member, address_attribute, None)
                deleted_addresses += 1

        for passenger in member.passengers:
            db.session.delete(passenger)
            deleted_passengers += 1

        db.session.delete(member)
    answer = raw_input("Deleting %s passengers and %s addresses, continue (y|n)?")
    if answer == "y":
        db.session.commit()
    else:
        db.session.rollback()




if __name__ == "__main__":
    manager.run()

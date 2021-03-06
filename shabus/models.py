from shabus import db
from flask.ext.security import UserMixin, RoleMixin

roles_users = db.Table("roles_users",
        db.Column("user_id", db.Integer(), db.ForeignKey("user_.id")),
        db.Column("role_id", db.Integer(), db.ForeignKey("role.id")))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name

class User(db.Model, UserMixin):
    __tablename__ = "user_"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref("users", lazy="dynamic"))

    def __repr__(self):
        return self.email

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, nullable=False)
    age = db.Column(db.String(255))
    email = db.Column(db.String(254), nullable=False, unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"), nullable=False)
    address = db.relationship("Address", foreign_keys=[address_id])
    additional_address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    additional_address = db.relationship("Address", foreign_keys=[additional_address_id])
    desired_destination_address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    desired_destination_address = db.relationship("Address", foreign_keys=[desired_destination_address_id])
    first_of_may = db.Column(db.Boolean(), nullable=False)
    desired_ride_time = db.Column(db.String(255))
    desired_board_time = db.Column(db.String(255))
    desired_return_time = db.Column(db.String(255))
    recommending_member_id = db.Column(db.Integer, db.ForeignKey("member.id"))
    recommending_member = db.relationship("Member", remote_side=[id], backref="recommended_members")
    legal_statement = db.Column(db.Text())
    signature_image_url = db.Column(db.String(255))
    backed_on_headstart = db.Column(db.Boolean(), nullable=False)
    used_old_form_to_sign_up = db.Column(db.Boolean(), nullable=False)
    credit_card_payment_products = db.Column(db.String(255))
    credit_card_payer_info = db.Column(db.String(255))
    credit_card_payer_address = db.Column(db.String(255))
    jotform_submission_id = db.Column(db.String(255))
    is_manager = db.Column(db.Boolean(), nullable=False)
    is_founder = db.Column(db.Boolean(), nullable=False)
    comments = db.Column(db.Text())

    def __repr__(self):
        return self.email

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    member = db.relationship("Member", backref="passengers", foreign_keys=[member_id])
    passenger_type = db.Column(db.Enum("member", "spouse", "child", name="passenger_types"), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255), unique=True)
    id_number = db.Column(db.String(255), unique=True)
    has_smartphone = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey("passenger.id"), nullable=False)
    passenger = db.relationship("Passenger", backref="rides", foreign_keys=[passenger_id])
    board_time = db.Column(db.DateTime, nullable=False)
    recorded_by_user_id = db.Column(db.Integer, db.ForeignKey("user_.id"), nullable=False)
    recorded_by_user = db.relationship("User", foreign_keys=[recorded_by_user_id])
    board_location = db.Column(db.String(255))

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255))
    number = db.Column(db.String(255))
    city = db.Column(db.String(255))
    neighborhood = db.Column(db.String(255))
    zipcode = db.Column(db.String(255))
    country = db.Column(db.String(255))

    def __repr__(self):
        return "%s %s, %s, %s" %  (self.street, self.number, self.city, self.country)

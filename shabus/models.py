from shabus import db
from flask.ext.security import UserMixin, RoleMixin

roles_users = db.Table("roles_users",
        db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
        db.Column("role_id", db.Integer(), db.ForeignKey("role.id")))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref("users", lazy="dynamic"))

    def __repr__(self):
        return "<User %s>" % (self.email)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_passenger_id = db.Column(db.Integer, db.ForeignKey("passenger.id"), unique=True)
    main_passenger = db.relationship("Passenger")
    created = db.Column(db.Timestsamp)

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"))
    category = db.relationship("Category", backref="passengers"))

    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey("passenger.id"))
    start_time = db.Column(db.Timestsamp)

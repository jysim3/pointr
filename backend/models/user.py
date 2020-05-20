from app import db

class Users(db.Model):
    __tablename__ = 'users'

    zid = db.Column(db.Text, primary_key=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    isarc = db.Column(db.Boolean, nullable=False)
    commencementyear = db.Column(db.Integer, nullable=False)
    studenttype = db.Column(db.Text, nullable=False)
    degreetype = db.Column(db.Text, nullable=False)
    superadmin = db.Column(db.Boolean, nullable=False)
    activated = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Text, nullable=True)
    additionalinformation = db.Column(db.JSON, nullable=True)
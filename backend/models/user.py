from app import db

class Users(db.Model):
    __tablename__ = 'users'

    zID = db.Column(db.Text, primary_key=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    preferredName = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=False)

    description = db.Column(db.Text, nullable=True)
    photo = db.Column(db.Text, nullable=True)
    isarc = db.Column(db.Boolean, nullable=False)

    commencementyear = db.Column(db.Integer, nullable=False)
    studenttype = db.Column(db.Text, nullable=False)
    degreetype = db.Column(db.Text, nullable=False)

    superadmin = db.Column(db.Boolean, nullable=False)
    activated = db.Column(db.Boolean, nullable=False)

    def jsonAttendanceFormat(self):
        return {
            'zID': self.zID,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'isarc': self.isarc
        }
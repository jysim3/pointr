from app import db
from models.event import interest

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

    attended = db.relationship("Attendance", back_populates="user")
    interested = db.relationship(
        "Event",
        secondary=interest,
        back_populates="interested"
    )
    staff = db.relationship("Staff", back_populates="user")

    def getPreview(self):
        return {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'photo': self.photo,
        }

    def jsonAttendanceFormat(self):
        return {
            'zID': self.zID,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'isarc': self.isarc
        }

    def getAttended(self):
        """
        Returns a list of objects of type Event that this user has went to
        """
        return [i.event for i in self.attended]

    def getAttendedIDs(self):
        """
        Returns a list of event IDs that this user has been to
        Lighter version of the function getEvents()
        """
        return [i.event.id for i in self.attended]

    def getAttendedJSON(self):
        """
        Returns a JSON array of the events' previews that this user has been to
        """
        return [i.getPreview() for i in self.attended]
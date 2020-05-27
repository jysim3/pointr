from app import db
from models.event import interest

class Users(db.Model):
    __tablename__ = 'users'

    zID = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    firstName = db.Column(db.Text, nullable=False)
    lastName = db.Column(db.Text, nullable=False)
    preferredName = db.Column(db.Text, nullable=True)

    photo = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    isArc = db.Column(db.Boolean, nullable=False)

    school = db.Column(db.Integer, nullable=False)
    faculty = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.Integer, nullable=False)
    commencementYear = db.Column(db.Integer, nullable=False)

    superadmin = db.Column(db.Boolean, nullable=False)
    activated = db.Column(db.Boolean, nullable=False)

    attended = db.relationship("Attendance", back_populates="user")
    interested = db.relationship(
        "Event",
        secondary=interest,
        back_populates="interested"
    )
    staff = db.relationship("Staff", back_populates="user")

    def getJSON(self):
        # NOTE: Think about using the .__dict__ method as opposed to doing this manually
        # TODO: COmplete this
        # Returns everything, including the events the user has attended and also the ones
        # he has expressed an interest for
        return {
            'zID': self.zID,
            'firstname': self.firstName,
            'lastname': self.lastName,
            'preferredName': self.preferredName,
            'description': self.description,
            'photo': self.photo,
            'isarc': self.isArc,
            'commencementyear': self.commencementYear,
            'school': self.school,
            'faculty': self.faculty,
            'degree': self.degree,
            'attended': [i.getPreview() for i in self.attended],
            'interested': [i.getPreview() for i in self.interested]
        }

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

    def getInterested(self):
        """
        Returns a list of objects of type Event that this user has expressed an interest to
        """
        return [i for i in self.interested]

    def addInterest(self, event):
        """
        Allows an user to express their interest for a particular event, events they are 
        interested in will send them notifications (probably, to be decided on the exact
        functionality)
        """
        # TODO:
        pass

    def addFollow(self, society):
        """
        Allows an user to follow a particular society, events hosted by socs they follow
        will be shown to them automatically
        """
        # TODO:
        pass

    @staticmethod
    def findUser(zID):
        user = Users.query.filter_by(zID=zID).first()
        return None if not user else user
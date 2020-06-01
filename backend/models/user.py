from app import db
from models.event import interest
from models.society import Staff

class Users(db.Model):
    __tablename__ = 'users'

    zID = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    firstName = db.Column(db.Text, nullable=False)
    lastName = db.Column(db.Text, nullable=False)
    preferredName = db.Column(db.Text, nullable=True)
    discordName = db.Column(db.Text, nullable=True)

    photo = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    isArc = db.Column(db.Boolean, nullable=False)

    school = db.Column(db.Integer, nullable=True)
    faculty = db.Column(db.Integer, nullable=True)
    degree = db.Column(db.Integer, nullable=True)
    commencementYear = db.Column(db.Integer, nullable=True)

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
            'attended': [i.event.getPreview() for i in self.attended],
            'interested': [i.getPreview() for i in self.interested]
        }

    def getPreview(self):
        return {
            'firstname': self.firstName,
            'lastname': self.lastName,
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
        self.interested.append(event)

        db.session.add(self)
        db.session.commit()

    def addFollow(self, society):
        """
        Allows an user to follow a particular society, events hosted by socs they follow
        will be shown to them automatically (NOTE: NOT IMPLEMENTED FOR THIS VERSION)
        """
        # TODO:
        pass

    def getUpcoming(self, show=5):
        """
        Returns all the events that this user's joined societies that are being hosted
        in the future, default to 5 events
        """
        events = []
        for i in self.staff:
            events.extend(i.society.getUpcomingEvents())

        events.sort(key=lambda event: event.start)
        return events[:show]

    def getUpcomingJSONs(self, show=5):
        """
        Same as getUpcoming() except that we return event preview jsons instead
        of event objects
        """
        events = []
        for i in self.staff:
            events.extend(i.society.getUpcomingEvents())

        events.sort(key=lambda event: event.start)

        return [i.getPreview() for i in events]

    def getPast(self, show=5):
        """
        Returns all the events that this user has attended
        default to 5 events
        """
        events = self.attended

        events.sort(key=lambda event: event.end, reversed=True)
        return events[:show]

    def getPastJSONs(self, show=5):
        """
        Same as getUpcoming() except that we return event preview jsons instead
        of event objects
        """
        events = self.attended

        events.sort(key=lambda event: event.end, reversed=True)
        return events[:show]

    def getSocs(self, json=False):
        """
        Returns a list of all socs that this user is participating in
        """
        members = Staff.query.filter_by(user=self, rank=0).all()
        admins = Staff.query.filter(Staff.user==self, Staff.rank>0).all()

        if json:
            members = [i.society.getSocietyJSON() for i in members]
            admins = [i.society.getSocietyJSON() for i in admins]
        else:
            members = [i.society for i in members]
            admins = [i.society for i in admins]
        return {'members': members, 'admins': admins}

    @staticmethod
    def findUser(zID):
        user = Users.query.filter_by(zID=zID).first()
        return None if not user else user
from app import db
from datetime import datetime

'''
class BaseEvent(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    start = db.Column(db.DateTime(timezone=True), nullable=True)
    end = db.Column(db.DateTime(timezone=True), nullable=True)

    hasQR = db.Column(db.Boolean, nullable=True)
    
    description = db.Column(db.Text, nullable=True)
    previewDescription = db.Column(db.Text, nullable=True)

    # TODO Consider and document functionality with admins
    closed = db.Column(db.Boolean, nullable=False)

    # TODO String Array
    photo = db.Column(db.Text, nullable=True)

    # NOTE: temporary Indiciates whether or not an event has request an access code feature
    temporary = db.Column(db.Boolean, nullable=False)
    accessCode = db.Column(db.Text, nullable=True)
'''


class CompositeEvent(db.Model):
    __tablename__ = "compositeEvents"

    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    start = db.Column(db.DateTime(timezone=True), nullable=False)
    end = db.Column(db.DateTime(timezone=True), nullable=False)

    photos = db.Column(db.ARRAY(db.Text), nullable=True)
    description = db.Column(db.Text, nullable=True)
    preview = db.Column(db.Text, nullable=True)
    location = db.Column(db.Text, nullable=True)

    # TODO: Add a relationshipo to connect requests
    # Requests is when a society asks another society to include this event
    # As part of the composite event
    #requests = db.Column(db.ARRAY(db.Text), nullable=True)
    
    status = db.Column(db.Text, nullable=False)
    tags = db.Column(db.ARRAY(db.Text), nullable=True)

    _events = db.relationship("Event", back_populates="_composite")

    def getEvents(self):
        return self._events

    def getEventsIDs(self):
        ids = []
        for i in self._events:
            ids.append(i.id)

        return ids

    def getEventsPreview(self):
        previews = []
        for i in self._events:
            previews.append(i.getPreview())

        return previews


class Attendance(db.Model):
    __tablename__ = 'attend'

    zID = db.Column(db.Text, db.ForeignKey('users.zID'), primary_key=True)
    eventID = db.Column(db.Text, db.ForeignKey('events.id'), primary_key=True)
    time = db.Column(db.DateTime(timezone=True), nullable=False, server_default=str(datetime.utcnow()))
    #firstname = db.Column(db.Text, nullable=False)
    #lastname = db.Column(db.Text, nullable=False)
    users = db.relationship("Users")

    def jsonifySelf(self):
        return {
            'zID': self.zID,
            'time': str(self.time),
            'firstname': self.users.firstname,
            'lastname': self.users.lastname
        }

class Interested(db.Model):
    __tablename__ = 'interested'
    zID = db.Column(db.Text, db.ForeignKey('users.zID'), primary_key=True)
    eventID = db.Column(db.Text, db.ForeignKey('events.id'), primary_key=True)

    users = db.relationship("Users")


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    start = db.Column(db.DateTime(timezone=True), nullable=False)
    end = db.Column(db.DateTime(timezone=True), nullable=False)

    photos = db.Column(db.ARRAY(db.Text), nullable=True)
    description = db.Column(db.Text, nullable=True)
    preview = db.Column(db.Text, nullable=True)
    location = db.Column(db.Text, nullable=True)

    hasQR = db.Column(db.Boolean, nullable=False)
    hasAccessCode = db.Column(db.Boolean, nullable=False)
    accessCode = db.Column(db.Text, nullable=True)
    hasAdminSignin = db.Column(db.Boolean, nullable=False)

    tags = db.Column(db.ARRAY(db.Text), nullable=True)

    status = db.Column(db.Text, nullable=False)

    compositeID = db.Column(db.Text, db.ForeignKey("compositeEvents.id"), nullable=False)
    _composite = db.relationship("CompositeEvent", back_populates="_events")

    attendances = db.relationship('Attendance')
    interested = db.relationship('Interested')

    def getPreview(self):
        payload = {}
        payload['id'] = self.id
        payload['name'] = self.name
        payload['logo'] = self.photos[0] if self.photos else None
        payload['preview'] = self.preview
        payload['startTime'] = self.start
        payload['location'] = self.location

        return payload

    def addAttendance(self, student):
        attend = Attendance(time=datetime.utcnow())
        attend.users = student
        self.attendances.append(attend)

        db.session.add(self)
        db.session.commit()

    def getAttendeeCSV(self):
        results = [i.jsonifySelf() for i in self.attendances]
        # TODO: COnver this to a CSV file, save it on the local directory and then
        # Serve up the path
        return results
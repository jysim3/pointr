from app import db

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


attendance = db.Table('attend',
    db.Column('zID', db.Text, db.ForeignKey('users.zID'), primary_key=True),
    db.Column('eventID', db.Text, db.ForeignKey('events.id'), primary_key=True)
)


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

    attendances = db.relationship('Users', secondary=attendance)

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
        self.attendances.append(student)
        db.session.add(self)
        db.session.commit()
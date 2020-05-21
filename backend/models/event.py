from app import db

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


class CompositeEvent(BaseEvent):

    def getEvents():
        ids = self.getEventIDs()
        # Do some stuff to get data we need

    def getEventsPreview():
        ids = self.getEventIDs()
        # Do some stuff to get just the preview icon and preview description

    def getEventIDs():
        pass

    def addEvent(id):
        pass

    # TODO Optimization
    def addEvents(ids):
        pass

    def removeEvent(id):
        pass

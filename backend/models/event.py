from app import db
from datetime import datetime
from models.society import host
from datetime import datetime, timezone, timedelta
import dateutil
from dateutil import parser
from hashlib import sha1

class Attendance(db.Model):
    __tablename__ = 'attend'

    eventID = db.Column(db.Text, db.ForeignKey('events.id'), primary_key=True)
    zID = db.Column(db.Text, db.ForeignKey('users.zID'), primary_key=True)
    time = db.Column(db.DateTime(timezone=True), nullable=False)

    user = db.relationship("Users", back_populates="attended")
    event = db.relationship("Event", back_populates="attendees")

    additionalInfo = db.Column(db.JSON, nullable=True)

    def jsonifySelf(self):
        return {
            'zID': self.zID,
            'time': str(self.time),
            'firstname': self.user.firstName,
            'lastname': self.user.lastName,
            'discordname': self.user.discordName if self.user.discordName else None,
            'isArc': self.user.isArc
        }

interest = db.Table('interested',
    db.Column('zID', db.Text, db.ForeignKey('users.zID'), primary_key=True),
    db.Column('eventID', db.Text, db.ForeignKey('events.id'), primary_key=True)
)


# TODO: Need a relationship to hook up compositeEvent with societies
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
        """
        Function to return all the events which belong to this composite event
        """
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

    additionalInfo = db.Column(db.JSON, nullable=True)

    tags = db.Column(db.ARRAY(db.Integer), nullable=True)

    status = db.Column(db.Integer, nullable=False)

    compositeID = db.Column(db.Text, db.ForeignKey("compositeEvents.id"), nullable=True)
    _composite = db.relationship("CompositeEvent", back_populates="_events")

    attendees = db.relationship("Attendance", back_populates="event")
    #attendances = db.relationship("Attendance")
    interested = db.relationship(
        'Users',
        secondary=interest,
        back_populates="interested"
    )
    hosting = db.relationship(
        'Societies',
        secondary=host,
        back_populates="hosting"
    )

    def getAttendCodes(self):
        seconds = datetime.now().timestamp() // 5 
        codes = [sha1(f"{seconds-i}{id}{'asdf'}".encode("UTF-8")).hexdigest()[:5]
            for i in range(3)]
        return codes
    def getAttendCode(self):
        seconds = datetime.now().timestamp() // 5 
        code = sha1(f"{seconds}{id}{'asdf'}".encode("UTF-8")).hexdigest()[:5]
        nextRefresh = (seconds+1) * 5
        return {
            'nextRefresh': nextRefresh,
            'code': code,
            'refreshInterval': 5000
        }
    def getPreview(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo': self.photos[0] if self.photos else None,
            'preview': self.preview,
            'startTime': self.start,
            'location': self.location
        }

    def getEventJSON(self):
        """
        Returns the full json of this event
        """
        return {
            'id': self.id,
            'name': self.name,
            'start': str(parser.parse(str(self.start)).astimezone(timezone.utc)),
            'end': str(parser.parse(str(self.end)).astimezone(timezone.utc)),
            'photos': self.photos,
            'description': self.description,
            'preview': self.preview,
            'location': self.location,
            'hasQR': self.hasQR,
            'hasAccessCode': self.hasAccessCode,
            'hasAdminSignin': self.hasAdminSignin,
            'tags': self.tags,
            'status': self.status,
            'society': [i.getPreview() for i in self.hosting]
        }

    def addAttendance(self, student):
        # TODO: Check whether current time is beyond the ending time
        if self.status == "closed":
            return "Event Closed"
        elif Attendance.query.filter_by(user=student, event=self).first():
            return "Already Attended"

        attend = Attendance(time=datetime.now(timezone.utc),
            user=student, event=self)

        db.session.add(attend)
        db.session.commit()

    def deleteAttendance(self, student):
        attend = Attendance.query.filter_by(user=student, event=self).first()
        if not attend:
            return "This user has not attended this event"

        db.session.delete(attend)
        db.session.commit()

    def addInterested(self, student):
        self.interested.append(student)

        db.session.add(self)
        db.session.commit()

    def getAttendanceJSON(self):
        results = [i.jsonifySelf() for i in self.attendees]
        return results

    def getAttended(self):
        """
        Returns a list of objects of type Users that have attended this event
        """
        return [i for i in self.attendees]

    def getInterested(self):
        """
        Returns a list of objects of type Users that has expressed interest in this event
        """
        return [i for i in self.interested]

    def closeEvent(self):
        self.status = "closed"

        db.session.add(self)
        db.session.commit()

    def getHostSoc(self):
        return self.hosting

    def addAdditionalInfo(self, payload):
        if not self.additionalInfo:
            self.additionalInfo = payload
        else:
            buffer = payload.copy()
            for key in payload.keys():
                if payload[key] in self.additionalInfo.values():
                    return "This question is already a part of the event"
                elif key in self.additionalInfo:
                    # Find how many of said key there are
                    counter = 0
                    for i in self.additionalInfo:
                        if i.find(key) != -1:
                            counter += 1
                    # We rename the key as key{the number of occurence}
                    buffer[f"{key}{counter}"] = buffer[key]
                    buffer.pop(key)

            payload = buffer
            # If we do this without the above lines, if the two have any keys of the exact same name,
            # The new value will write over the old value
            self.additionalInfo = {**self.additionalInfo, **payload}

        db.session.add(self)
        db.session.commit()

    def deleteAdditionalInfo(self, payload):
        if not self.additionalInfo:
            return "No additional information required for this event"
        else:
            buffer = self.additionalInfo.copy()
            for value in payload.values():
                if value not in self.additionalInfo.values():
                    continue
                else:
                    for k, v in self.additionalInfo.items():
                        if v == value:
                            # We can get away with this since event's won't have the same questions twice
                            buffer.pop(k)
                            self.additionalInfo = buffer

                            db.session.add(self)
                            db.session.commit()

                            return

        return "This event doesn't have this question set yet"

    def updateAdditionalInfo(self, oldPayload, newPayload):
        # TODO: Finish this route
        pass

    @staticmethod
    def getEventsByTag(tag):
        # TODO
        return 0

    @staticmethod
    def getEvent(id):
        event = Event.query.filter_by(id=id).first()
        return None if not event else event

    @staticmethod
    def getAllEvents():
        events = Event.query.all()
        return events

    @staticmethod
    def getAllUpcomingEvents(offset=5):
        events = Event.query.filter(Event.start>datetime.now(timezone.utc)).all()
        return events[:offset]

    @staticmethod
    def getAllUpcomingEventsJSONs(offset=5):
        events = Event.query.filter(Event.start>datetime.now(timezone.utc)).all()
        events.sort(key=lambda event: event.start)
        return [event.getPreview() for event in events][:offset]

    @staticmethod
    def getAllEventsPreviews():
        events = Event.query.all()
        events.sort(key=lambda event: event.start)
        return [event.getPreview() for event in events]

    @staticmethod
    def deleteEvent(event):
        db.session.delete(event)
        db.session.commit()
from app import db
from datetime import datetime
from pytz import timezone
from constants import PUBLIC, PRIVATE, UNLISTED

host = db.Table('hosted',
    db.Column('eventID', db.Text, db.ForeignKey('events.id'), primary_key=True),
    db.Column('socID', db.Text, db.ForeignKey('societies.id'), primary_key=True)
)

# Colleges cannot be joined but other societies can be (colleges are given set list of members)
# Join type: Invitation/Admin Approval/Anyone

class Societies(db.Model):
    __tablename__ = "societies"

    id = db.Column(db.Text, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=False)
    
    previewDescription = db.Column(db.Text, nullable=True)

    photo = db.Column(db.Text, nullable=True)

    type = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.ARRAY(db.Integer))

    # TODO: Need something here to indicate the type of society
    # I.e. invitational, etc.

    # Relationship-related
    staff = db.relationship("Staff", back_populates="society")
    hosting = db.relationship(
        'Event',
        secondary=host,
        back_populates="hosting"
    )

    def getPreview(self):
        return {
            'id': self.id,
            'description': self.description,
            'name': self.name
        }

    def getSocietyJSON(self):
        return {
            'id': self.id,
            'description': self.description,
            'name': self.name,
            'previewDescription': self.previewDescription,
            'photo': self.photo,
            'type': self.type,
            'tags': self.tags
        }

    def addStaff(self, user, role=0):
        staff = Staff.query.filter_by(user=user, society=self).first()
        if staff:
            if role:
                staff.role = role
                db.session.add(staff)
                db.session.commit()
                return
            return "Already a member of the society"

        newStaff = Staff(rank=role, user=user, society=self)

        db.session.add(newStaff)
        db.session.commit()

    def deleteStaff(self, user, role=None):
        staff = Staff.query.filter_by(user=user, society=self).first()

        if not staff:
            return "Not a member of this society"

        if not role:
            db.session.delete(staff)
            db.session.commit()
        else:
            staff.rank = role

    def getMembers(self):
        """
        Returns a list of objects of type Users which are members/admins of this society
        """
        members = Staff.query.filter_by(rank=0, society=self).all()
        return [i.user.getPreview() for i in members]

    def getMembersCount(self):
        return len(Staff.query.filter(Staff.rank>=0, Staff.society==self).all())

    def getMembersIDs(self):
        """
        Returns a list of user zIDs in string format which are members of this society)
        """
        members = Staff.query.filter_by(rank=0, society=self).all()
        return [i.user.zID for i in members]

    def getAdmins(self):
        admins = Staff.query.filter(Staff.rank>=1, Staff.society==self).all()
        return [i.user.getPreview() for i in admins]

    def getAdminsIDs(self):
        admins = Staff.query.filter(Staff.rank>=1, Staff.society==self).all()
        return [i.user.zID for i in admins]

    def isMember(self, user):
        return True if Staff.query.filter(Staff.rank>=0, Staff.user==user, Staff.society==self).first() else False

    def isAdmin(self, user):
        return True if Staff.query.filter(Staff.rank>=1, Staff.user==user, Staff.society==self).first() else False

    # TODO: COnsider refactoring isMember, isAdmin into one function
    # TODO: Also consider whether or not we should have use a Staff.query or just iterate
    # through the staff table

    def getEvents(self):
        """
        Returns a list of objects of type events that this society is hosting
        """
        return [i for i in self.hosting]

    def getEventsIDs(self):
        """
        Returns a list of eventIDs of type strings that this society is hosting
        """
        return [i.id for i in self.hosting]

    def getUpcomingEvents(self, privacy=PUBLIC):
        """
        Returns a list of objects of type events that this society has upcoming
        """
        currentTime = datetime.now(timezone('utc'))
        events = []
        for i in self.hosting:
            if i.start > currentTime and ((not i.privacy) or i.privacy <= privacy):
                events.append(i)
        return sorted(events, key=lambda event: event.start)

    def getPastEvents(self):
        """
        Returns a list of objects of type events that this society has upcoming
        """
        currentTime = datetime.now(timezone('utc'))
        events = []
        for i in self.hosting:
            if i.start < currentTime:
                events.append(i)
        return sorted(events, key=lambda event: event.start, reverse=True)

    def getLogo(self):
        """
        Returns the path of which the soc logo is located at
        """
        return self.photo

    def removeLogo(self):
        """
        Clear the path of the soc logo (i.e. delete the soc logo)
        """
        self.photo = None

        db.session.add(self)
        db.session.commit()

    def setLogo(self, logo):
        self.photo = logo

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def findSociety(id):
        society = Societies.query.filter_by(id=id).first()
        return None if not society else society

    @staticmethod
    def getSocietyByName(name):
        society = Societies.query.filter_by(name=name).first()
        return None if not society else society

    @staticmethod
    def getAllSocieties(json=False):
        societies = Societies.query.all()

        if json:
            return [i.getSocietyJSON() for i in societies]

        return societies

    @staticmethod
    def getSocietiesByTag(tag):
        taggedSocs = Societies.query.filter(Societies.tags.any(tag)).all()
        return taggedSocs

class Staff(db.Model):
    __tablename__ = 'staff'

    zID = db.Column(db.Text, db.ForeignKey('users.zID'), primary_key=True)
    socID = db.Column(db.Text, db.ForeignKey('societies.id'), primary_key=True)
    rank = db.Column(db.Integer, nullable=False)

    user = db.relationship("Users", back_populates="staff")
    society = db.relationship("Societies", back_populates="staff")

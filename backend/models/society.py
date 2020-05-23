from app import db

# Colleges cannot be joined but other societies can be (colleges are given set list of members)
# Join type: Invitation/Admin Approval/Anyone


host = db.Table('hosted',
    db.Column('eventID', db.Text, db.ForeignKey('events.id'), primary_key=True),
    db.Column('socID', db.Text, db.ForeignKey('societies.id'), primary_key=True)
)

class Societies(db.Model):
    __tablename__ = "societies"

    id = db.Column(db.Text, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    
    description = db.Column(db.Text, nullable=True)
    previewDescription = db.Column(db.Text, nullable=True)

    # TODO String Array
    photo = db.Column(db.Text, nullable=True)

    # TODO: Need something here to indicate the type of society
    # I.e. invitational, etc.

    # Relationship-related
    staff = db.relationship("Staff", back_populates="society")
    hosting = db.relationship(
        'Event',
        secondary=host,
        back_populates="hosting"
    )

    def addStaff(self, user, role=0):
        if Staff.query.filter_by(user=user, society=self).first():
            return "Already a member of the society"

        newStaff = Staff(rank=role, user=user, society=self)

        db.session.add(newStaff)
        db.session.commit()

    def getMembers(self):
        """
        Returns a list of objects of type Users which are members/admins of this society
        """
        members = Staff.query.filter_by(rank=0).all()
        return [i.user.getPreview() for i in members]

    def getAdmins(self):
        admins = Staff.query.filter(Staff.rank>=1).all()
        return [i.user.getPreview() for i in admins]

    def isMember(self, user):
        return True if Staff.query.filter(Staff.rank>=0, Staff.user==user).first() else False

    def isAdmin(self, user):
        return True if Staff.query.filter(Staff.rank>=1, Staff.user==user).first() else False

    # TODO: COnsider refactoring isMember, isAdmin into one function

class Staff(db.Model):
    __tablename__ = 'staff'

    zID = db.Column(db.Text, db.ForeignKey('users.zID'), primary_key=True)
    socID = db.Column(db.Text, db.ForeignKey('societies.id'), primary_key=True)
    rank = db.Column(db.Integer, nullable=False)

    user = db.relationship("Users", back_populates="staff")
    society = db.relationship("Societies", back_populates="staff")

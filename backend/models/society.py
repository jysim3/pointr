from app import db

# Colleges cannot be joined but other societies can be (colleges are given set list of members)
# Join type: Invitation/Admin Approval/Anyone

class Societies(db.Model):
    __tablename__ = "societies"

    id = db.Column(db.Text, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    
    description = db.Column(db.Text, nullable=True)
    previewDescription = db.Column(db.Text, nullable=True)

    # TODO String Array
    photo = db.Column(db.Text, nullable=True)

    # NOTE: isCollege will be replaced with an additional table instead to maintain
    # maximum generalisation
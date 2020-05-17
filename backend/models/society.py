from app import db

class Societies(db.Model):
    __tablename__ = "societies"

    id = db.Column(db.Text, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    additionalInformation = db.Column(db.JSON, nullable=True)

    # NOTE: isCollege will be replaced with an additional table instead to maintain
    # maximum generalisation
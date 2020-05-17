from app import db

class Events(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    startTime = db.Column(db.DateTime(timezone=True), nullable=True)
    endTime = db.Column(db.DateTime(timezone=True), nullable=True)
    week = db.Column(db.Text, nullable=False)
    qrCode = db.Column(db.Boolean, nullable=True)
    description = db.Column(db.Text, nullable=True)
    closed = db.Column(db.Boolean, nullable=False)
    # NOTE: temporary Indiciates whether or not an event has request an access code feature
    temporary = db.Column(db.Boolean, nullable=False)
    accessCode = db.Column(db.Text, nullable=True)
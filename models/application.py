from extensions import db
from datetime import datetime

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drive.id"))
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Applied")  # Applied/Shortlisted/Selected/Rejected

    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),)
from extensions import db
from flask_login import UserMixin

class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # profile fields
    department = db.Column(db.String(50))
    cgpa = db.Column(db.Float)
    backlogs = db.Column(db.Integer, default=0)
    arrear_history = db.Column(db.String(5), default="No")
    tenth_percentage = db.Column(db.Float)
    twelfth_percentage = db.Column(db.Float)
    resume = db.Column(db.String(200))
    photo = db.Column(db.String(200))                      
    profile_completed = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    applications = db.relationship("Application", backref="student", cascade="all, delete")

    def get_id(self):
        return f"student-{self.id}"
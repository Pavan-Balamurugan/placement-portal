from extensions import db
from flask_login import UserMixin

class Company(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    hr_contact = db.Column(db.String(50))
    website = db.Column(db.String(200))
    approval_status = db.Column(db.String(20), default="Pending")
    is_active = db.Column(db.Boolean, default=True)

    drives = db.relationship("PlacementDrive", backref="company", cascade="all, delete")

    def get_id(self):
        return f"company-{self.id}"

    def __repr__(self):
        return f"<Company {self.company_name}>"
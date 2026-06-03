from extensions import db
from flask_login import UserMixin

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def get_id(self):
        return f"admin-{self.id}"
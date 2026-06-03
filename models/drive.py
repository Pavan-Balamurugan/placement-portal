from extensions import db

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(150))
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(50), default="Pending")  # Pending/Approved/Closed/Rejected

    # NEW: Job details
    required_skills = db.Column(db.Text)        # comma-separated skills
    experience = db.Column(db.String(100))       # e.g. "0-1 years", "Fresher"
    salary_range = db.Column(db.String(100))     # e.g. "4-6 LPA"

    # Eligibility
    min_cgpa = db.Column(db.Float, default=0.0)
    allowed_departments = db.Column(db.Text)     # CSV string
    max_backlogs = db.Column(db.Integer, default=0)
    require_no_arrears = db.Column(db.String(5), default="No")  # Yes/No
    min_tenth = db.Column(db.Float, default=0.0)
    min_twelfth = db.Column(db.Float, default=0.0)

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    applications = db.relationship("Application", backref="drive", cascade="all, delete")

from flask import Flask
from extensions import db, login_manager
import os


@login_manager.user_loader
def load_user(user_id):
    from models.student import Student
    from models.company import Company
    from models.user import Admin

    role, id = user_id.split("-")
    id = int(id)

    if role == "admin":
        return db.session.get(Admin, id)
    elif role == "student":
        return db.session.get(Student, id)
    elif role == "company":
        return db.session.get(Company, id)

    return None

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads/resumes'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"


    from models.user import Admin
    from models.student import Student
    from models.company import Company
    from models.drive import PlacementDrive
    from models.application import Application

    from routes.auth_routes import auth_bp
    from routes.admin_routes import admin_bp
    from routes.company_routes import company_bp
    from routes.student_routes import student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)

    with app.app_context():
        db.create_all()


        if not Admin.query.first():
            admin = Admin(username="admin", password="admin123")
            db.session.add(admin)
            db.session.commit()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
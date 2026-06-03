from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.student import Student
from models.company import Company
from models.user import Admin
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return redirect(url_for("auth.login"))


@auth_bp.route("/register-student", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/register_student.html")

        existing = Student.query.filter_by(email=email).first()
        if existing:
            flash("An account with this email already exists.", "danger")
            return render_template("auth/register_student.html")

        student = Student(
            name=name,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(student)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register_student.html")


@auth_bp.route("/register-company", methods=["GET", "POST"])
def register_company():
    if request.method == "POST":
        company_name = request.form.get("company_name")
        email = request.form.get("email")
        password = request.form.get("password")
        hr_contact = request.form.get("hr_contact")
        website = request.form.get("website")

        if not company_name or not email or not password:
            flash("Company name, email, and password are required.", "danger")
            return render_template("auth/register_company.html")

        existing = Company.query.filter_by(email=email).first()
        if existing:
            flash("An account with this email already exists.", "danger")
            return render_template("auth/register_company.html")

        company = Company(
            company_name=company_name,
            email=email,
            password=generate_password_hash(password),
            hr_contact=hr_contact,
            website=website
        )
        db.session.add(company)
        db.session.commit()

        flash("Registration successful! Please wait for admin approval before logging in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register_company.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("identifier")
        password = request.form.get("password")

        # Check admin (plain comparison — admin is seeded manually)
        admin = Admin.query.filter_by(username=identifier).first()
        if admin and admin.password == password:
            login_user(admin)
            return redirect(url_for("admin.dashboard"))

        # Check student
        student = Student.query.filter_by(email=identifier).first()
        if student and check_password_hash(student.password, password):
            if not student.is_active:
                flash("Your account has been deactivated. Contact admin.", "danger")
                return render_template("auth/login.html")
            login_user(student)
            return redirect(url_for("student.student_dashboard"))

        # Check company
        company = Company.query.filter_by(email=identifier).first()
        if company and check_password_hash(company.password, password):
            if not company.is_active:
                flash("Your company account has been deactivated. Contact admin.", "danger")
                return render_template("auth/login.html")
            if company.approval_status != "Approved":
                flash("Your company registration is pending admin approval.", "warning")
                return render_template("auth/login.html")
            login_user(company)
            return redirect(url_for("company.company_dashboard"))

        flash("Invalid credentials. Please try again.", "danger")
        return render_template("auth/login.html")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))

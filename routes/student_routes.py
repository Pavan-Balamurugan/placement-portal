import os
from flask import Blueprint, render_template, redirect, url_for, abort, request, current_app, flash
from flask_login import login_required, current_user
from models.student import Student
from models.drive import PlacementDrive
from models.company import Company
from models.application import Application
from extensions import db
from werkzeug.utils import secure_filename

student_bp = Blueprint("student", __name__, url_prefix="/student")

ALLOWED_PHOTO_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_photo(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_PHOTO_EXTENSIONS


@student_bp.route("/dashboard")
@login_required
def student_dashboard():
    if not isinstance(current_user, Student):
        abort(403)

    search = request.args.get("search", "").strip()

    query = PlacementDrive.query.filter_by(status="Approved")

    if search:
        query = query.filter(
            db.or_(
                PlacementDrive.job_title.ilike(f"%{search}%"),
                PlacementDrive.company.has(Company.company_name.ilike(f"%{search}%"))
            )
        )

    drives = query.all()
    applications = Application.query.filter_by(student_id=current_user.id).all()
    application_map = {app.drive_id: app.status for app in applications}

    return render_template(
        "student/dashboard.html",
        drives=drives,
        application_map=application_map,
        search=search
    )


@student_bp.route("/apply/<int:drive_id>")
@login_required
def apply_drive(drive_id):
    if not isinstance(current_user, Student):
        abort(403)

    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.status != "Approved":
        flash("This drive is not open for applications.", "danger")
        return redirect(url_for("student.student_dashboard"))

    if not current_user.profile_completed:
        flash("Please complete your profile before applying.", "warning")
        return redirect(url_for("student.profile"))

    # Eligibility checks
    allowed = (drive.allowed_departments or "").split(",")
    if "All" not in allowed and current_user.department not in allowed:
        flash("You are not eligible: your department is not allowed for this drive.", "danger")
        return redirect(url_for("student.student_dashboard"))

    if (current_user.cgpa or 0.0) < (drive.min_cgpa or 0.0):
        flash(f"You are not eligible: minimum CGPA required is {drive.min_cgpa}.", "danger")
        return redirect(url_for("student.student_dashboard"))

    if (current_user.backlogs or 0) > (drive.max_backlogs or 0):
        flash(f"You are not eligible: maximum backlogs allowed is {drive.max_backlogs}.", "danger")
        return redirect(url_for("student.student_dashboard"))

    if drive.require_no_arrears == "Yes" and (current_user.arrear_history or "No") == "Yes":
        flash("You are not eligible: this drive requires no arrear history.", "danger")
        return redirect(url_for("student.student_dashboard"))

    if (current_user.tenth_percentage or 0.0) < (drive.min_tenth or 0.0):
        flash(f"You are not eligible: minimum 10th percentage required is {drive.min_tenth}.", "danger")
        return redirect(url_for("student.student_dashboard"))

    if (current_user.twelfth_percentage or 0.0) < (drive.min_twelfth or 0.0):
        flash(f"You are not eligible: minimum 12th percentage required is {drive.min_twelfth}.", "danger")
        return redirect(url_for("student.student_dashboard"))

    existing = Application.query.filter_by(student_id=current_user.id, drive_id=drive_id).first()
    if existing:
        flash("You have already applied for this drive.", "warning")
        return redirect(url_for("student.student_dashboard"))

    application = Application(student_id=current_user.id, drive_id=drive_id)
    db.session.add(application)
    db.session.commit()

    flash("Application submitted successfully!", "success")
    return redirect(url_for("student.student_applications"))


@student_bp.route("/applications")
@login_required
def student_applications():
    if not isinstance(current_user, Student):
        abort(403)

    applications = (
        Application.query
        .filter_by(student_id=current_user.id)
        .order_by(Application.application_date.desc())
        .all()
    )

    return render_template("student/applications.html", applications=applications)


@student_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if not isinstance(current_user, Student):
        abort(403)

    if request.method == "POST":
        department = request.form.get("department")

        if not department:
            return render_template("student/profile.html", error="Please select a department.")

        current_user.department = department
        current_user.cgpa = float(request.form.get("cgpa") or 0)
        current_user.backlogs = int(request.form.get("backlogs") or 0)
        current_user.arrear_history = request.form.get("arrear_history")
        current_user.tenth_percentage = float(request.form.get("tenth_percentage") or 0)
        current_user.twelfth_percentage = float(request.form.get("twelfth_percentage") or 0)

        # Handle photo upload
        photo = request.files.get("photo")
        if photo and photo.filename and allowed_photo(photo.filename):
            ext = photo.filename.rsplit(".", 1)[1].lower()
            filename = f"student_{current_user.id}_photo.{ext}"
            photo_folder = os.path.join("static", "uploads", "photos")
            os.makedirs(photo_folder, exist_ok=True)
            photo.save(os.path.join(photo_folder, filename))
            current_user.photo = filename

        current_user.profile_completed = True
        db.session.commit()

        flash("Profile updated successfully!", "success")
        return redirect(url_for("student.student_dashboard"))

    return render_template("student/profile.html", error=None)


@student_bp.route("/complete-profile")
@login_required
def complete_profile():
    return redirect(url_for("student.profile"))


@student_bp.route("/upload-resume", methods=["GET", "POST"])
@login_required
def upload_resume():
    if not isinstance(current_user, Student):
        abort(403)

    if request.method == "POST":
        file = request.files.get("resume")

        if not file or not file.filename:
            flash("Please select a file to upload.", "danger")
            return redirect(url_for("student.upload_resume"))

        if not file.filename.lower().endswith(".pdf"):
            flash("Only PDF files are allowed.", "danger")
            return redirect(url_for("student.upload_resume"))

        filename = f"student_{current_user.id}_resume.pdf"
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        path = os.path.join(upload_folder, filename)
        file.save(path)

        current_user.resume = filename
        db.session.commit()

        flash("Resume uploaded successfully!", "success")
        return redirect(url_for("student.student_dashboard"))

    return render_template("student/upload_resume.html")

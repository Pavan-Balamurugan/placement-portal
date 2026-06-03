from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from models.company import Company
from models.drive import PlacementDrive
from models.application import Application
from extensions import db
from datetime import datetime

company_bp = Blueprint("company", __name__, url_prefix="/company")


@company_bp.route("/dashboard")
@login_required
def company_dashboard():
    if not isinstance(current_user, Company):
        abort(403)

    drives = PlacementDrive.query.filter_by(company_id=current_user.id).all()
    return render_template("company/dashboard.html", drives=drives)


@company_bp.route("/profile", methods=["GET", "POST"])
@login_required
def company_profile():
    if not isinstance(current_user, Company):
        abort(403)

    if request.method == "POST":
        company_name = request.form.get("company_name")

        if not company_name:
            flash("Company name cannot be empty.", "danger")
            return render_template("company/profile.html")

        current_user.company_name = company_name
        current_user.hr_contact = request.form.get("hr_contact", "").strip()
        current_user.website = request.form.get("website", "").strip()

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("company.company_dashboard"))

    return render_template("company/profile.html")


@company_bp.route("/create-drive", methods=["GET", "POST"])
@login_required
def create_drive():
    if not isinstance(current_user, Company):
        abort(403)

    if current_user.approval_status != "Approved":
        flash("Your company must be approved by admin before posting drives.", "danger")
        return redirect(url_for("company.company_dashboard"))

    if request.method == "POST":
        job_title = request.form.get("job_title")
        description = request.form.get("description")
        required_skills = request.form.get("required_skills")
        experience = request.form.get("experience")
        salary_range = request.form.get("salary_range")
        min_cgpa = request.form.get("min_cgpa")
        allowed_departments_list = request.form.getlist("allowed_departments")
        max_backlogs = request.form.get("max_backlogs")
        require_no_arrears = request.form.get("require_no_arrears")
        min_tenth = request.form.get("min_tenth")
        min_twelfth = request.form.get("min_twelfth")
        deadline_str = request.form.get("deadline")

        if not allowed_departments_list:
            return render_template("company/create_drive.html",
                                   error="Please select at least one department.")

        allowed_departments = ",".join(allowed_departments_list)

        deadline = None
        if deadline_str:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")

        drive = PlacementDrive(
            job_title=job_title,
            description=description,
            required_skills=required_skills,
            experience=experience,
            salary_range=salary_range,
            min_cgpa=float(min_cgpa) if min_cgpa else 0.0,
            allowed_departments=allowed_departments,
            max_backlogs=int(max_backlogs) if max_backlogs else 0,
            require_no_arrears=require_no_arrears,
            min_tenth=float(min_tenth) if min_tenth else 0.0,
            min_twelfth=float(min_twelfth) if min_twelfth else 0.0,
            deadline=deadline,
            company_id=current_user.id
        )

        db.session.add(drive)
        db.session.commit()

        flash("Placement drive submitted for admin approval.", "success")
        return redirect(url_for("company.company_dashboard"))

    return render_template("company/create_drive.html", error=None)


@company_bp.route("/drive/<int:drive_id>/edit", methods=["GET", "POST"])
@login_required
def edit_drive(drive_id):
    if not isinstance(current_user, Company):
        abort(403)

    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        abort(403)

    if drive.status == "Closed":
        flash("Cannot edit a closed drive.", "warning")
        return redirect(url_for("company.company_dashboard"))

    if request.method == "POST":
        allowed_departments_list = request.form.getlist("allowed_departments")

        if not allowed_departments_list:
            return render_template("company/edit_drive.html",
                                   drive=drive,
                                   error="Please select at least one department.")

        drive.job_title = request.form.get("job_title")
        drive.description = request.form.get("description")
        drive.required_skills = request.form.get("required_skills")
        drive.experience = request.form.get("experience")
        drive.salary_range = request.form.get("salary_range")
        drive.min_cgpa = float(request.form.get("min_cgpa") or 0)
        drive.allowed_departments = ",".join(allowed_departments_list)
        drive.max_backlogs = int(request.form.get("max_backlogs") or 0)
        drive.require_no_arrears = request.form.get("require_no_arrears")
        drive.min_tenth = float(request.form.get("min_tenth") or 0)
        drive.min_twelfth = float(request.form.get("min_twelfth") or 0)

        deadline_str = request.form.get("deadline")
        if deadline_str:
            drive.deadline = datetime.strptime(deadline_str, "%Y-%m-%d")

        drive.status = "Pending"
        db.session.commit()

        flash("Drive updated and resubmitted for admin approval.", "success")
        return redirect(url_for("company.company_dashboard"))

    return render_template("company/edit_drive.html", drive=drive, error=None)


@company_bp.route("/drive/<int:drive_id>/applications")
@login_required
def view_drive_applications(drive_id):
    if not isinstance(current_user, Company):
        abort(403)

    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        abort(403)

    applications = Application.query.filter_by(drive_id=drive.id).all()
    return render_template("company/applications.html", drive=drive, applications=applications)


@company_bp.route("/drive/<int:drive_id>/close")
@login_required
def close_drive(drive_id):
    if not isinstance(current_user, Company):
        abort(403)

    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        abort(403)

    drive.status = "Closed"
    db.session.commit()

    flash("Drive closed successfully.", "success")
    return redirect(url_for("company.company_dashboard"))


@company_bp.route("/drive/<int:drive_id>/delete")
@login_required
def delete_drive(drive_id):
    if not isinstance(current_user, Company):
        abort(403)

    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        abort(403)

    db.session.delete(drive)
    db.session.commit()

    flash("Drive deleted.", "success")
    return redirect(url_for("company.company_dashboard"))


@company_bp.route("/application/<int:app_id>/update/<string:new_status>")
@login_required
def update_application_status(app_id, new_status):
    if not isinstance(current_user, Company):
        abort(403)

    application = Application.query.get_or_404(app_id)
    drive = PlacementDrive.query.get(application.drive_id)

    if drive.company_id != current_user.id:
        abort(403)

    allowed_statuses = ["Shortlisted", "Selected", "Rejected"]
    if new_status in allowed_statuses:
        application.status = new_status
        db.session.commit()
        flash(f"Application marked as {new_status}.", "success")
    else:
        flash("Invalid status.", "danger")

    return redirect(url_for("company.view_drive_applications", drive_id=application.drive_id))

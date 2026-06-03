from flask import Blueprint, render_template, abort, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models.user import Admin
from models.company import Company
from models.student import Student
from models.drive import PlacementDrive
from models.application import Application
from extensions import db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if not isinstance(current_user, Admin):
        abort(403)

    total_companies = Company.query.count()
    total_students = Student.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()

    return render_template(
        "admin/dashboard.html",
        total_companies=total_companies,
        total_students=total_students,
        total_drives=total_drives,
        total_applications=total_applications
    )


@admin_bp.route("/companies")
@login_required
def view_companies():
    if not isinstance(current_user, Admin):
        abort(403)

    search = request.args.get("search", "").strip()
    if search:
        companies = Company.query.filter(
            Company.company_name.ilike(f"%{search}%")
        ).all()
    else:
        companies = Company.query.all()

    return render_template("admin/companies.html", companies=companies, search=search)


@admin_bp.route("/company/<int:company_id>/approve")
@login_required
def approve_company(company_id):
    if not isinstance(current_user, Admin):
        abort(403)

    company = Company.query.get_or_404(company_id)
    company.approval_status = "Approved"
    db.session.commit()

    flash(f"{company.company_name} has been approved.", "success")
    return redirect(url_for("admin.view_companies"))


@admin_bp.route("/company/<int:company_id>/reject")
@login_required
def reject_company(company_id):
    if not isinstance(current_user, Admin):
        abort(403)

    company = Company.query.get_or_404(company_id)
    company.approval_status = "Rejected"
    db.session.commit()

    flash(f"{company.company_name} has been rejected.", "warning")
    return redirect(url_for("admin.view_companies"))


@admin_bp.route("/company/<int:company_id>/delete")
@login_required
def delete_company(company_id):
    if not isinstance(current_user, Admin):
        abort(403)

    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()

    flash("Company deleted successfully.", "success")
    return redirect(url_for("admin.view_companies"))


@admin_bp.route("/company/<int:company_id>/blacklist")
@login_required
def blacklist_company(company_id):
    if not isinstance(current_user, Admin):
        abort(403)

    company = Company.query.get_or_404(company_id)
    company.is_active = not company.is_active
    db.session.commit()

    status = "unblocked" if company.is_active else "blacklisted"
    flash(f"{company.company_name} has been {status}.", "warning")
    return redirect(url_for("admin.view_companies"))


@admin_bp.route("/drives")
@login_required
def view_drives():
    if not isinstance(current_user, Admin):
        abort(403)

    drives = PlacementDrive.query.all()
    return render_template("admin/drives.html", drives=drives)


@admin_bp.route("/drive/<int:drive_id>/approve")
@login_required
def approve_drive(drive_id):
    if not isinstance(current_user, Admin):
        abort(403)

    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = "Approved"
    db.session.commit()

    flash(f'Drive "{drive.job_title}" has been approved.', "success")
    return redirect(url_for("admin.view_drives"))


@admin_bp.route("/drive/<int:drive_id>/reject")
@login_required
def reject_drive(drive_id):
    if not isinstance(current_user, Admin):
        abort(403)

    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = "Rejected"
    db.session.commit()

    flash(f'Drive "{drive.job_title}" has been rejected.', "warning")
    return redirect(url_for("admin.view_drives"))


@admin_bp.route("/drive/<int:drive_id>/delete")
@login_required
def delete_drive(drive_id):
    if not isinstance(current_user, Admin):
        abort(403)

    drive = PlacementDrive.query.get_or_404(drive_id)
    db.session.delete(drive)
    db.session.commit()

    flash("Drive deleted.", "success")
    return redirect(url_for("admin.view_drives"))


@admin_bp.route("/students")
@login_required
def view_students():
    if not isinstance(current_user, Admin):
        abort(403)

    search = request.args.get("search", "").strip()

    if search:
        filters = [
            Student.name.ilike(f"%{search}%"),
            Student.email.ilike(f"%{search}%"),
        ]
        # Only add ID filter if search is a valid integer
        if search.isdigit():
            filters.append(Student.id == int(search))

        students = Student.query.filter(db.or_(*filters)).all()
    else:
        students = Student.query.all()

    return render_template("admin/students.html", students=students, search=search)


@admin_bp.route("/student/<int:student_id>/blacklist")
@login_required
def blacklist_student(student_id):
    if not isinstance(current_user, Admin):
        abort(403)

    student = Student.query.get_or_404(student_id)
    student.is_active = not student.is_active
    db.session.commit()

    status = "unblocked" if student.is_active else "blacklisted"
    flash(f"{student.name} has been {status}.", "warning")
    return redirect(url_for("admin.view_students"))


@admin_bp.route("/student/<int:student_id>/delete")
@login_required
def delete_student(student_id):
    if not isinstance(current_user, Admin):
        abort(403)

    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully.", "success")
    return redirect(url_for("admin.view_students"))


@admin_bp.route("/applications")
@login_required
def view_applications():
    if not isinstance(current_user, Admin):
        abort(403)

    applications = Application.query.all()
    return render_template("admin/applications.html", applications=applications)

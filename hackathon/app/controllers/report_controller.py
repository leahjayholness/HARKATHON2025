from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)
from sqlalchemy import exc
from app.models.report import Report
from app.controllers.authentication_controller import login_required
from app import db

report_bp = Blueprint("report", __name__)

@report_bp.route("/", methods=["GET"])
@login_required
def list_reports():
    if g.user.is_admin:
        reports = Report.query.all()
    else:
        reports = Report.query.filter_by(account_id=session.get("user_id")).all()
    return render_template("report/reports.html", reports=reports)

@report_bp.route("/create", methods=("GET", "POST"))
@login_required
def create_report():
    if request.method == "POST":
        _title = request.form.get('issue')
        _content = request.form.get('message')
        error = None

        if not _title or not _content:
            error = "All fields are required."
        
        if error is None:
            new_report = Report(
                title=_title,
                content=_content,
                account_id=session.get('user_id'),
                account=g.user
            )
            db.session.add(new_report)
            db.session.commit()
            return redirect(url_for("index"))
        
        flash(error)
        
    return render_template("report/create.html")

@report_bp.route("/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit_report(id):
    report = Report.query.get(id)
    if not g.user.is_admin:
        flash("You are not authorized to edit this report.")
        return redirect(url_for("index"))

    if request.method == "POST":
        _title = request.form.get('issue')
        _content = request.form.get('message')
        error = None

        if not _title or not _content:
            error = "All fields are required."

        if error is None:
            report.title = _title
            report.content = _content
            db.session.commit()
            flash("Report updated successfully!")
            return redirect(url_for("index"))

        flash(error)

    return render_template("report/edit.html", report=report)

@report_bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete_report(id):
    report = Report.query.get(id)
    if not g.user.is_admin:
        flash("You are not authorized to delete this report.")
        return redirect(url_for("index"))

    db.session.delete(report)
    db.session.commit()
    flash("Report deleted successfully!")
    return redirect(url_for("index"))
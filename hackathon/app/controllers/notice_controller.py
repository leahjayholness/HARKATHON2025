from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)
from sqlalchemy import exc
from app.models.notice import Notice
from app.controllers.authentication_controller import login_required
from app import db

notice_bp = Blueprint("notice", __name__)

@notice_bp.route("/", methods=("GET",))
@login_required
def list_notices():
    notices = Notice.query.all()
    return render_template("notice/noticeboard.html", notices=notices)

@notice_bp.route("/create", methods=("GET", "POST"))
@login_required
def create_notice():
    if request.method == "POST":
        _title = request.form.get('title')
        _content = request.form.get('content')
        error = None

        if not _title or not _content:
            error = "All fields are required."
        
        if error is None:
            new_notice = Notice(
                title=_title,
                content=_content
            )
            db.session.add(new_notice)
            db.session.commit()
            return redirect(url_for("index"))
        
        flash(error)
        
    return render_template("notice/create.html")

@notice_bp.route("/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit_notice(id):
    notice = Notice.query.get(id)
    if not g.user.is_admin:
        flash("You are not authorized to edit this notice.")
        return redirect(url_for("index"))

    if request.method == "POST":
        _title = request.form.get('title')
        _content = request.form.get('content')
        error = None

        if not _title or not _content:
            error = "All fields are required."

        if error is None:
            notice.title = _title
            notice.content = _content
            db.session.commit()
            flash("Notice updated successfully!")
            return redirect(url_for("index"))

        flash(error)

    return render_template("notice/edit.html", notice=notice)

@notice_bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete_notice(id):
    notice = Notice.query.get(id)
    if not g.user.is_admin:
        flash("You are not authorized to delete this notice.")
        return redirect(url_for("index"))

    db.session.delete(notice)
    db.session.commit()
    flash("Notice deleted successfully!")
    return redirect(url_for("index"))
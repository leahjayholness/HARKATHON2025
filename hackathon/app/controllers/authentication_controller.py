import functools

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)


from sqlalchemy import exc
from app import bcrypt
from app.models.account import Account
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        _username = request.form['username']
        _password = request.form['password']
        _name = request.form['name']
        _hall = request.form['hall']
        _email = request.form['email']
        error = None

        if not _username:
            error = 'Username is required.'
        elif not _password:
            error = 'Password is required.'
        elif not _name:
            error = 'Name is required.'
        elif not _hall:
            error = 'Hall is required.'
        elif not _email:
            error = 'Email is required.'

        if error is None:
            try:
                _is_admin = Account.query.first() == None
                account = Account(
                    username = _username,
                    password = bcrypt.generate_password_hash(_password).decode('utf-8'),
                    name = _name,
                    hall = _hall,
                    email = _email,
                    is_admin = _is_admin
                )
                db.session.add(account)
                db.session.commit()
            except exc.IntegrityError:
                error = f"User {_username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        try:
            account = db.session.execute(db.select(Account).filter_by(username=username)).scalar_one()
        except exc.NoResultFound:
            error = 'Incorrect username.'
        else:
            if not bcrypt.check_password_hash(account.password, password):
                error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = account.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@auth_bp.before_app_request
def load_logged_in_user():
    account_id = session.get('user_id')

    if account_id is None:
        g.user = None
    else:
        g.user = Account.query.get(account_id)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Must be logged in.")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

from flask import Blueprint, jsonify, request, flash, render_template
from app.models.account import Account
from app.controllers.authentication_controller import login_required
from app import db
from sqlalchemy import exc

# Create a blueprint for account-related routes
account_bp = Blueprint("account", __name__)

@account_bp.route("/")
@login_required
def list_accounts():
    accounts = Account.query.all()
    return jsonify([{"name": a.name, "username": a.username, "hall": a.hall} for a in accounts])

@account_bp.route("/<int:id>")
@login_required
def account_details(id):
    account = Account.query.get(id)
    return jsonify({"name": account.name, "email": account.email})

@account_bp.route('/loyalty')
@login_required
def loyalty():
    return render_template('account/loyal.html')

def add_points(account:Account):
    account.points += 5
    check_status(account)

def check_status(account:Account):
    # Update status based on points
    if account.points >= 400:
        account.status = 'Free Wash And Dry!'
    elif account.points >= 200:
        account.status = 'Free Wash Or Dry!'
    elif account.points >= 100:
        account.status = '50 Percent Off Next Wash Or Dry!'
    elif account.points >= 50:
        account.status = '20 Percent Off Next Wash Or Dry!'
    else:
        account.status = 'No Discount Yet'
    
    db.session.commit()

def redeem_points(account:Account, reward):
    # Redeem points for rewards
    if account.points >= reward['points']:
        account.points -= reward['points']
        account.rewards.append(reward)
        account.check_status()  # Update status after redeeming
        flash(f"{account.name} redeemed {reward['name']} for {reward['points']} points.")
        return True
    flash(f"{account.name} does not have enough points to redeem {reward['name']}.")
    return False
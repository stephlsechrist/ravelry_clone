from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import User, Yarn, Needle
from . import db

views = Blueprint("views", __name__)

# below is how to create flask route/endpoint
@views.route("/")
@views.route("/home")
@login_required
def home():
    stash = Yarn.query.all()
    needles = Needle.query.all()
    # can pass information from back end to front end
    # left is name to be used in rendered template, right is the info being passed
    return render_template("home.html", user=current_user, stash=stash, needles=needles)

# TODO: much later, add search function
@views.route("/stash")
@login_required
def stash():
    stash=Yarn.query.all()
    return render_template("stash.html", user=current_user, stash=stash)

# TODO: update db (only add for now), return redirect to /stash
@views.route("/update-stash", methods=['GET', 'POST'])
@login_required
def update_stash():
    stash = Yarn.query.all()
    
    if request.method == "POST":
        brand = request.form.get('brand')
        color = request.form.get('color')
        weight = request.form.get('weight')
        material = request.form.get('material')
        amount = request.form.get('amount')
        if not brand:
            flash('Brand cannot be empty', category='error')
        elif not color:
            flash('Color cannot be empty', category='error')
        elif not weight:
            flash('Weight cannot be empty', category='error')
        else:
            yarn = Yarn(brand=brand, color=color, weight=weight, material=material, amount=amount, user=current_user.id)
            db.session.add(yarn)
            db.session.commit()
            flash('Yarn added!', category='success')
            return redirect(url_for('views.stash'))
    
    return render_template("update-stash.html", user=current_user, stash=stash)
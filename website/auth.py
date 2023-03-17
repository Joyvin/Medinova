from io import BytesIO
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from .models import User, Upload
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, login_user, current_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        key = str(password)
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, key):
                flash('Logged In Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!, Try Again!', category='error')
        else:
            flash('Email does not exist!', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2= request.form.get('password2')
        mail = str(email)
        uname = str(username)
        pass1 = str(password1)
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif len(mail) < 4: 
            flash('Email must be greater than 3 characters.', category='error')
        elif len(uname) < 2: 
            flash('First name must be greater than 1 character.', category='error')
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(pass1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # add user to database
            new_user = User(email=email, username=username, password=generate_password_hash(pass1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home')) # views.py --> home() function
            # OR return redirect('/')
    return render_template("signup.html", user=current_user)

# @auth.route('/fill_details', methods=['GET', 'POST'])
# @login_required
# def fill_details():
    # if request.method == 'POST':
#     return render_template("fill_details.html", user=current_user)

@auth.route('/fill_details', methods=['GET', 'POST'])
# @login_required
def fill_details():
    if request.method == 'POST':
        image_file = request.files['image_file']
        upload = Upload(filename=image_file.filename, data=image_file.read())
        db.session.add(upload)
        db.session.commit()
        return f'Uploaded: {image_file.filename}'
    return render_template("fill_details.html", user=current_user)

# @auth.route('/download/<upload_id>', methods=['GET', 'POST'])
# @login_required
# def download(upload_id):
#     upload = Upload.query.filter_by(id=upload_id).first()
#     return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)
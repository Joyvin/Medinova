from io import BytesIO
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from .models import User, Upload
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename

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
                if user.id != 1:
                    return redirect('/')
                else:
                    return redirect('/admin')
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
            if new_user.id != 1:
                new_user.person = "User"
                db.session.add(new_user)
                db.session.commit()
                return redirect('/')
            else:
                new_user.person = "Admin"
                db.session.add(new_user)
                db.session.commit()                
                return redirect('/admin')
    return render_template("signup.html", user=current_user)

# @auth.route('/fill_details', methods=['GET', 'POST'])
# @login_required
# def fill_details():
    # if request.method == 'POST':
#     return render_template("fill_details.html", user=current_user)

@auth.route('/fill_details', methods=['GET', 'POST'])
@login_required
def fill_details():
    if request.method == 'POST':
        image_file = request.files['image_file']
        if not image_file:
            return 'No image uploaded!', 400
        pdf_file = request.files['pdf_file']
        if not pdf_file:
            return 'No pdf uploaded!', 400
        image_mimetype = image_file.mimetype
        pdf_mimetype = pdf_file.mimetype
        my_name = request.form['my_name']
        emer_name = request.form['emer_name']
        emer_phone = request.form['emer_phone']
        emer_email = request.form['emer_email']
        upload = Upload(image_file=secure_filename(image_file.filename), image_data=image_file.read(), image_mimetype=image_mimetype, pdf_file=secure_filename(pdf_file.filename), pdf_data=pdf_file.read(), pdf_mimetype=pdf_mimetype, my_name=my_name, emer_name=emer_name, emer_email=emer_email, emer_phone=emer_phone, user_id=current_user.id)
        db.session.add(upload)
        db.session.commit()
        flash(f'Uploaded: {image_file.filename} and {pdf_file.filename}', category='success')
        # return redirect(url_for('views.home'))
    return render_template("fill_details.html", user=current_user)

# @auth.route('/download/<upload_id>', methods=['GET', 'POST'])
# @login_required
# def download(upload_id):
#     upload = Upload.query.filter_by(id=upload_id).first()
#     return send_file(BytesIO(upload.image_data), attachment_filename=upload.image_file, as_attachment=True)
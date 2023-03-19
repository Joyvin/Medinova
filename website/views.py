from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Upload, Diabetes, Heart, Park, Note, Appoint, To_Dos
import requests
from . import db
from .diabetes import my_diabetes
from .heart import my_heart
from .parkinson import my_park
import json
import datetime
from azure.storage.blob import BlobServiceClient
import random

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    return render_template("about.html", user=current_user)

@views.route('/landing')
def landing():
    return render_template("Landingpg.html")

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@views.route('/admin_board', methods=['GET', 'POST'])
@login_required
def admin_board():
    return render_template("admin_board.html", user=current_user)

@views.route('/records', methods=['GET', 'POST'])
@login_required
def records():
    return render_template("records.html", user=current_user)

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.id == 1: 
        return render_template("admin.html", user=current_user)
    else:
        return 

@views.route('/storage')
def index():
    blob_service_client = BlobServiceClient(account_url="https://medistorage.blob.core.windows.net/", credential="Wkgdqz4BTnzbN3DdmxIpvDAsV7Y0H2yW489m0AFggD+iEsSmeISD5MWNtICaagrPVLLlq2b9pPGd+AStKALxBA==")
    container_client = blob_service_client.get_container_client(container='imgs')

    blob_list = container_client.list_blobs()
    dirs = [i.split('/')[1] for i in blob_list if i.name.split('/')[0] == current_user.username]
    print(dirs)
    return render_template("storage.html", user=current_user, dirs=dirs)

def scan(src):
    url = "https://medinova-func.azurewebsites.net/api/medifunc?task=face"

    users = [f"https://medistorage.blob.core.windows.net/imgs/{i.username}-face.jpeg" for i in User.query.all()]

    payload = json.dumps({
    "src": src,
    "faces": users
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    uname = response.text.split('/').pop().split('-')[0] 

    return(uname)

@views.route('/fill_details', methods=['GET', 'POST'])
def fill_details():
    if request.method == 'POST':
        if(Upload.query.filter_by(user_id=current_user.id).count() > 0):
            upload = Upload.query.filter_by(user_id=current_user.id).first()
            emy_name= upload.my_name
            eage= upload.age
            edob= upload.dob
            egender= upload.gender
            eheight= upload.height
            eweight= upload.weight
            eblood_grp= upload.blood_grp
            eheart_attack= upload.heart_attack
            eregion= upload.region
            epincode= upload.pincode
            eallergies= upload.allergies
            emedic= upload.medic
            epast_medic= upload.past_medic
            db.session.delete(upload)
            db.session.commit()
        else:
            emy_name= ""
            eage= ""
            edob= ""
            egender= ""
            eheight= ""
            eweight= ""
            eblood_grp= ""
            eheart_attack= ""
            eregion= ""
            epincode= ""
            eallergies= ""
            emedic= ""
            epast_medic= ""
        
        if request.form.get('my_name', None): 
            my_name = request.form['my_name']
        else:
            my_name = emy_name
        if request.form.get('age', None):
            age = request.form['age']
        else:
            age = eage
        if request.form.get('dob', None):
            dob = request.form['dob']
        else:
            dob = edob
        if request.form.get('gender', None):
            gender = request.form['gender']
        else:
            gender = egender
        if request.form.get('height', None):
            height = request.form['height']
        else:
            height = eheight
        if request.form.get('weight', None): 
            weight = request.form['weight']
        else:
            weight = eweight
        if request.form.get('blood_grp', None): 
            blood_grp = request.form['blood_grp']
        else:
            blood_grp = eblood_grp
        if request.form.get('heart_attack', None): 
            heart_attack = request.form['heart_attack']
        else:
            heart_attack = eheart_attack
        if request.form.get('region', None): 
            region = request.form['region']
        else:
            region = eregion
        if request.form.get('pincode', None): 
            pincode = request.form['pincode']
        else:
            pincode = epincode
        if request.form.get('allergies', None): 
            allergies = request.form['allergies']
        else:
             allergies = eallergies
        if request.form.get('medic', None): 
            medic = request.form['medic']
        else:
            medic = emedic
        if request.form.get('past_medic', None): 
            past_medic = request.form['past_medic']
        else:
            past_medic = epast_medic
        new_upload = Upload(my_name=my_name, age=age, dob=dob, gender=gender, height=height, weight=weight,  blood_grp=blood_grp, heart_attack=heart_attack, region=region, pincode=pincode, allergies=allergies, medic=medic, past_medic=past_medic, user_id = current_user.id)
        db.session.add(new_upload)
        db.session.commit()
    return render_template("fill_details.html", user=current_user)

@views.route('/diabetes', methods=['POST', 'GET'])
def diabetes():
    if request.method == 'POST':
        pregnancies = float(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        bloodpressure = float(request.form['bloodpressure'])
        skinthickness = float(request.form['skinthickness'])
        insulin = float(request.form['insulin'])
        BMI = float(request.form['BMI'])
        DiabetesPedigreeFunction = request.form['DiabetesPedigreeFunction']
        age = float(request.form['age'])
        pred_diabetes = my_diabetes(pregnancies, glucose, bloodpressure, skinthickness, insulin, BMI, DiabetesPedigreeFunction, age)
        new_diabetes = Diabetes(pregnancies=pregnancies, glucose=glucose, bloodpressure=bloodpressure, skinthickness=skinthickness, insulin=insulin, BMI=BMI, DiabetesPedigreeFunction=DiabetesPedigreeFunction, age=age, pred_diabetes=pred_diabetes[0], user_id = current_user.id)
        db.session.add(new_diabetes)
        db.session.commit()
        if pred_diabetes[0] == 1:
            flash('You can have Diabetes', category="error")
            print("Probability for diabetes: ", pred_diabetes[1])
            # return redirect('/diab_yes')
        else: 
            flash('You cannot have Diabetes', category="success")
            # return redirect('/diab_no')
    return render_template('diabetes_form.html', user=current_user)

@views.route('/heart', methods=['POST', 'GET'])
def heart():
    if request.method == 'POST':
        age = float(request.form['age'])
        s = request.form['sex']
        if s == 'M':
            sex = 1.0
        else:
            sex = 0.0
        cp = float(request.form['cp'])
        rbp = float(request.form['rbp'])
        chol = float(request.form['chol'])
        fbs = float(request.form['fbs'])
        recg = float(request.form['recg'])
        mhra = float(request.form['mhra'])
        exia = float(request.form['exia'])
        oldpeak = float(request.form['oldpeak'])
        slope = float(request.form['slope'])
        vcf = float(request.form['vcf'])
        thal = float(request.form['thal'])
        pred_heart = my_heart(age, sex, cp, rbp, chol, fbs, recg, mhra, exia, oldpeak, slope, vcf, thal)
        new_heart = Heart(age=age, sex=sex, cp=cp, rbp=rbp, chol=chol, fbs=fbs, recg=recg, mhra=mhra, exia=exia, oldpeak=oldpeak, slope=slope, vcf=vcf, thal=thal, pred_heart=pred_heart[0], user_id = current_user.id)
        db.session.add(new_heart)
        db.session.commit()
        if pred_heart[0] == 1:
            flash("You can have Heart Disease.", category="error")

        else: 
            flash('You cannot have Heart Disease', category="success")
    return render_template('heart_form.html', user=current_user)

@views.route('/checkFace', methods=['POST'])
def check():
    image_file = request.files['image_file']
    if not image_file:
        return 'No image uploaded!', 400
    else:
        name = current_user.username + '-detect-'+ str(random.randint(10000, 99999)) +'.jpeg'
        blob_service_client = BlobServiceClient(account_url="https://medistorage.blob.core.windows.net/", credential="Wkgdqz4BTnzbN3DdmxIpvDAsV7Y0H2yW489m0AFggD+iEsSmeISD5MWNtICaagrPVLLlq2b9pPGd+AStKALxBA==")
        blob_client = blob_service_client.get_blob_client(container="imgs", blob = name)
        blob_client.upload_blob(image_file.read())
        res = scan(f"https://medistorage.blob.core.windows.net/imgs/{name}")
        user = User.query.filter_by(username = res).first()
        return render_template('records.html', user=user)

@views.route('/uploadFile', methods=['POST'])
def upload():
    image_file = request.files['image_file']
    if not image_file:
        return 'No image uploaded!', 400
    else:
        blob_service_client = BlobServiceClient(account_url="https://medistorage.blob.core.windows.net/", credential="Wkgdqz4BTnzbN3DdmxIpvDAsV7Y0H2yW489m0AFggD+iEsSmeISD5MWNtICaagrPVLLlq2b9pPGd+AStKALxBA==")
        blob_client = blob_client = blob_service_client.get_blob_client(container="imgs", blob = current_user.username + '/' + image_file.filename)
        blob_client.upload_blob(image_file.read())
        return redirect('/storage')

@views.route('/park', methods=['POST', 'GET'])
def park():
    if request.method == 'POST':
        mdvp_fo = float(request.form['mdvp_fo'])
        mdvp_fhi = float(request.form['mdvp_fhi'])
        mdvp_flo = float(request.form['mdvp_flo'])
        mdvp_jitter = float(request.form['mdvp_jitter'])
        mdvp_jitter_abs = float(request.form['mdvp_jitter_abs'])
        mdvp_rap = float(request.form['mdvp_rap'])
        mdvp_ppq = float(request.form['mdvp_ppq'])
        jitter_ddp = float(request.form['jitter_ddp'])
        mdvp_shimmer = float(request.form['mdvp_shimmer'])
        mdvp_shimmer_db = float(request.form['mdvp_shimmer_db'])
        mdvp_shimmer_apq3 = float(request.form['mdvp_shimmer_apq3'])
        mdvp_shimmer_apq5 = float(request.form['mdvp_shimmer_apq5'])
        mdvp_apq = float(request.form['mdvp_apq'])
        shimmer_dda = float(request.form['shimmer_dda'])
        nhr = float(request.form['nhr'])
        hnr = float(request.form['hnr'])
        rpde = float(request.form['rpde'])
        dfa = float(request.form['dfa'])
        spread1 = float(request.form['spread1'])
        spread2 = float(request.form['spread2'])
        d2 = float(request.form['d2'])
        ppe = float(request.form['ppe'])
        pred_park = my_park(mdvp_fo, mdvp_fhi, mdvp_flo, mdvp_jitter, mdvp_jitter_abs, mdvp_rap, mdvp_ppq, jitter_ddp, mdvp_shimmer, mdvp_shimmer_db, mdvp_shimmer_apq3, mdvp_shimmer_apq5, mdvp_apq, shimmer_dda, nhr, hnr, rpde, dfa, spread1, spread2, d2, ppe)
        new_park = Park(mdvp_fo=mdvp_fo, mdvp_fhi=mdvp_fhi, mdvp_flo=mdvp_flo, mdvp_jitter=mdvp_jitter, mdvp_jitter_abs=mdvp_jitter_abs, mdvp_rap=mdvp_rap, mdvp_ppq=mdvp_ppq, jitter_ddp=jitter_ddp, mdvp_shimmer=mdvp_shimmer, mdvp_shimmer_db=mdvp_shimmer_db, mdvp_shimmer_apq3=mdvp_shimmer_apq3, mdvp_shimmer_apq5=mdvp_shimmer_apq5, mdvp_apq=mdvp_apq, shimmer_dda=shimmer_dda, nhr=nhr, hnr=hnr, rpde=rpde, spread2=spread2, d2=d2, dfa=dfa, ppe=ppe, pred_park=pred_park[0], user_id = current_user.id)
        db.session.add(new_park)
        db.session.commit()
        if pred_park[0] == 1:
            flash('You can have Parkinson Disease', category="error")
        else: 
            flash('You cannot have Parkinson Disease', category="success")
    return render_template('parkinson_form.html', user=current_user)

@views.route('/analytical_tests', methods=['GET', 'POST'])
def analytics():
    return render_template("analytical_tests.html", user=current_user)

@views.route('/note', methods=['GET', 'POST'])
def note():
    if request.method == 'POST':
        note = request.form.get('note')
        my_note = str(note)
        if len(my_note) < 1:
            flash("Note is too short!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category='success')
    return render_template("notes.html", user=current_user)

@views.route('/todo', methods=['GET', 'POST'])
def todo_html():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if len(title) < 1 or len(desc) < 1:
            flash("ToDo is too short!", category='error')
        else:
            todo = To_Dos(title=title, desc=desc, user_id=current_user.id)
            db.session.add(todo)
            db.session.commit()
            flash("Todo added!", category='success')
    return render_template("todo.html", user=current_user)

@views.route('/update/<int:id>', methods=['GET', 'POST'])
def update_todo(id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = To_Dos.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/todo')
    todo = To_Dos.query.filter_by(id=id).first()
    return render_template("update.html", todo=todo, user=current_user)

@views.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_profile(id):
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        user = User.query.filter_by(id=id).first()
        user.firstname = firstname
        user.lastname = lastname
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    user = User.query.filter_by(id=id).first()
    return render_template("edit_profile.html", user=current_user)

@views.route('/delete/<int:id>')
def delete_todo(id):
    todo = To_Dos.query.filter_by(id=id).first()
    if todo.user_id == current_user.id:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/todo')
    todo = To_Dos.query.filter_by(id=id).first()
    return render_template("todo.html", todo=todo, user=current_user)

@views.route('/appoint', methods=['GET', 'POST'])
def appoint_html():
    if request.method == 'POST':
        t = request.form['t']
        d = request.form['d']
        # ti = str(t)
        # de = str(d)
        if len(t) < 1 or len(d) < 1:
            flash("Appointment is too short!", category='error')
        else:
            appointed = Appoint(t=t, d=d, user_id=current_user.id)
            db.session.add(appointed)
            db.session.commit()
            flash("Appointment added!", category='success')
    return render_template("appointment.html", user=current_user)

@views.route('/appoint_update/<int:id>', methods=['GET', 'POST'])
def update_appoint(id):
    if request.method == 'POST':
        t = request.form['t']
        d = request.form['d']
        appointed = Appoint.query.filter_by(id=id).first()
        appointed.t = t
        appointed.d = d
        db.session.add(appointed)
        db.session.commit()
        return redirect('/appoint')
    appointed = Appoint.query.filter_by(id=id).first()
    return render_template("appoint_update.html", appointed=appointed, user=current_user)

@views.route('/appoint_delete/<int:id>')
def delete_appoint(id):
    appointed = Appoint.query.filter_by(id=id).first()
    if appointed.user_id == current_user.id:
        db.session.delete(appointed)
        db.session.commit()
        return redirect('/appoint')
    appointed = Appoint.query.filter_by(id=id).first()
    return render_template("appointment.html", appointed=appointed, user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            redirect('notes.html')
    return jsonify({})

@views.route('/diab_reversal')
def diab_reversal():
    return render_template("diab_reversal.html", user=current_user)

@views.route('/diab_yes')
def diab_yes():
    return render_template("diab_popup_yes.html", user=current_user)

@views.route('/diab_no')
def diab_no():
    return render_template("diab_popup_no.html", user=current_user)
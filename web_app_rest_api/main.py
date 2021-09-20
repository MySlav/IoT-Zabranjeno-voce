# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 13:23:12 2021

@author: Mislav
"""
#import torchvision

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required
from . import db
from .models import Voce, Popusti, Opazaji
from os import getcwd
from os.path import join
from sqlalchemy.exc import SQLAlchemyError
from base64 import b64encode, b64decode
from sqlalchemy.sql import text
from datetime import datetime
from PIL import Image
from io import BytesIO
from albumentations import Compose, SmallestMaxSize, CenterCrop, Normalize
from albumentations.pytorch import ToTensorV2
from torch import load, no_grad, exp
from torch import max as tmax
from numpy import asarray

main = Blueprint('main', __name__)

# ML model

transform = Compose([SmallestMaxSize(224), CenterCrop(224, 224),
                     Normalize(mean=(0.485, 0.456, 0.406),
                               std=(0.229, 0.224, 0.225)),
                     ToTensorV2()
                     ])

modelML = load(getcwd()+'/model/final_model.pth', map_location='cpu')


def evaluation(model, image):
    model.eval()
    image = image.unsqueeze_(0)
    with no_grad():
        ps = exp(model.forward(image))
        _, predTest = tmax(ps, 1)
    return predTest


@main.route('/', methods=['GET'])
@login_required
def Index():
    all_data = Voce.query.all()

    return render_template("index.html", voca=all_data)


@main.route('/discounts', methods=['GET'])
@login_required
def Discounts():
    all_data = Popusti.query.all()

    return render_template("discounts.html", popusti=all_data)


@main.route('/observations', methods=['GET'])
@login_required
def Observations():
    all_data = Opazaji.query.all()

    return render_template("observations.html", opazaji=all_data)

# New Fruit


@main.route('/voce/insert', methods=['POST'])
@login_required
def add_voce():
    if request.method == 'POST':
        Ime = request.form['Ime']
        slika = request.files['slika']
        BeaconUUID = request.form['BeaconUUID']
        BeaconMajor = request.form['BeaconMajor']
        BeaconMinor = request.form['BeaconMinor']
        OsnovnaCijena = request.form['OsnovnaCijena']
        TrenutnaKlasa = request.form['TrenutnaKlasa']
        slika = b64encode(slika.read()).decode('ascii')
        novo_voce = Voce(Ime, slika, BeaconUUID, BeaconMajor,
                         BeaconMinor, OsnovnaCijena, TrenutnaKlasa)
        db.session.add(novo_voce)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('main.Index'))

        flash("Fruit Inserted Successfully")

        return redirect(url_for('main.Index'))

# Update Fruit


@main.route('/voce/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        global data
        my_data = Voce.query.get(request.form.get('ID'))
        my_data.Ime = request.form['Ime']
        my_data.BeaconUUID = request.form['BeaconUUID']
        my_data.BeaconMajor = request.form['BeaconMajor']
        my_data.BeaconMinor = request.form['BeaconMinor']
        my_data.OsnovnaCijena = request.form['OsnovnaCijena']
        my_data.TrenutnaKlasa = request.form['TrenutnaKlasa']
        data = my_data
        if request.files['slika'].filename != '':
            my_data.slika = request.files['slika']
            my_data.slika = b64encode(my_data.slika.read()).decode('ascii')
            data = my_data.slika
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('main.Index'))
        flash("Fruit Updated Successfully")

        return redirect(url_for('main.Index'))

# Delete Fruit


@main.route('/voce/delete/<ID>', methods=['GET', 'POST'])
@login_required
def delete(ID):
    my_data = Voce.query.get(ID)
    db.session.delete(my_data)
    try:
        db.session.commit()
        with db.engine.connect() as connection:
            connection.execute(text("""declare @max int;  
                                    select @max = max(ID) from Voce;  
                                    dbcc checkident(Voce,reseed,@max);"""))
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash(error)
        return redirect(url_for('main.Index'))
    flash("Fruit Deleted Successfully")

    return redirect(url_for('main.Index'))

# New Discount


@main.route('/discount/insert', methods=['POST'])
@login_required
def add_popust():
    if request.method == 'POST':
        ID_voce = request.form['ID_voce']
        Ime_Klase = request.form['Ime_Klase']
        Klasa = request.form['Klasa']
        Popust = request.form['Popust']

        novi_popust = Popusti(ID_voce, Ime_Klase, Klasa, Popust)
        db.session.add(novi_popust)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('main.Discounts'))

        flash("Discount Inserted Successfully")

        return redirect(url_for('main.Discounts'))

# Update Discount


@main.route('/discount/update', methods=['GET', 'POST'])
@login_required
def update_disc():
    if request.method == 'POST':
        my_data = Popusti.query.get(request.form.get('ID'))
        my_data.ID_voce = request.form['ID_voce']
        my_data.Ime_Klase = request.form['Ime_Klase']
        my_data.Klasa = request.form['Klasa']
        my_data.Popust = request.form['Popust']
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('main.Discounts'))
        flash("Discount Updated Successfully")

        return redirect(url_for('main.Discounts'))

# Delete Discount


@main.route('/discount/delete/<ID>', methods=['GET', 'POST'])
@login_required
def delete_disc(ID):
    my_data = Popusti.query.get(ID)
    db.session.delete(my_data)
    try:
        db.session.commit()
        with db.engine.connect() as connection:
            connection.execute(text("""declare @max int;  
                                    select @max = max(ID) from Popusti;  
                                    dbcc checkident(Popusti,reseed,@max);"""))

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash(error)
    flash("Discount Deleted Successfully")
    

    return redirect(url_for('main.Discounts'))

# New Observation


@main.route('/observation/insert', methods=['POST'])
@login_required
def add_opazaj():
    if request.method == 'POST':
        ID_voca = request.form['ID_voca']
        slikaPI = request.files['slikaPI']
        KlasaModel = request.form['KlasaModel']
        Vrijeme = request.form['Vrijeme'].replace("T", " ")
        slikaPI = b64encode(slikaPI.read()).decode('ascii')
        novi_opazaj = Opazaji(ID_voca, slikaPI, KlasaModel, Vrijeme)
        db.session.add(novi_opazaj)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('main.Observations'))
        flash("Observation Inserted Successfully")

        return redirect(url_for('main.Observations'))

# Update Observation


@main.route('/observation/update', methods=['GET', 'POST'])
@login_required
def update_obs():
    if request.method == 'POST':
        my_data = Opazaji.query.get(request.form.get('ID'))
        my_data.ID_voca = request.form['ID_voca']
        my_data.KlasaModel = request.form['KlasaModel']
        my_data.Vrijeme = request.form['Vrijeme'].replace("T", " ")
        if request.files['slikaPI'].filename != '':
            my_data.slikaPI = request.files['slikaPI']
            my_data.slikaPI = b64encode(my_data.slikaPI.read()).decode('ascii')
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('main.Observations'))
        flash("Observation Updated Successfully")

        return redirect(url_for('main.Observations'))

# Delete Observation


@main.route('/observation/delete/<ID>', methods=['GET', 'POST'])
@login_required
def delete_obs(ID):
    my_data = Opazaji.query.get(ID)
    db.session.delete(my_data)
    try:
        db.session.commit()
        with db.engine.connect() as connection:
            connection.execute(text("""declare @max int;  
                                    select @max = max(ID) from Opazaji;  
                                    dbcc checkident(Opazaji,reseed,@max);"""))
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash(error)
        return redirect(url_for('main.Observations'))
    flash("Observation Deleted Successfully")

    return redirect(url_for('main.Observations'))

# Send UUID and back info


@main.route('/api/beacon', methods=['GET'])
def beacon():
    if 'UUID' and 'Major' and 'Minor' in request.args:
        UUID = str(request.args['UUID'])
        Major = str(request.args['Major'])
        Minor = str(request.args['Minor'])
    else:
        return 'Please provide BeaconUUID Major and Minor in query string'

    with db.engine.connect() as connection:
        result = connection.execute(text("""SELECT V.[ID], V.[Ime], V.[TrenutnaKlasa], P.[Popust], V.[OsnovnaCijena] FROM [dbo].[Voce] 
                                         V INNER JOIN [dbo].[Popusti] P ON V.[ID] = P.[ID_voce]  
                                         WHERE [BeaconUUID]=:UUID  AND [BeaconMajor]=:Major AND [BeaconMinor]=:Minor AND V.[TrenutnaKlasa] = P.[Klasa]"""),
                                    UUID=UUID, Major=Major, Minor=Minor)
        result_dict = [{column: value for column, value in row.items()}
                       for row in result]
        result_dict[0]["Popust"] = str(result_dict[0]["Popust"])
        result_dict[0]["OsnovnaCijena"] = str(result_dict[0]["OsnovnaCijena"])

        if result_dict:
            return result_dict[0]
        else:
            return 'No fruit assigned to this Beacon UUID, Major and Minor combination'


@main.route('/api/uploadPI', methods=['POST'])
def uploadPI():
    data = request.json
    if 'ID_voca' and 'slikaPI' and 'KlasaModel' in data:
        ID_voca = str(data['ID_voca'])
        slikaPI = str(data['slikaPI'])
        KlasaModel = str(data['KlasaModel'])
    else:
        return 'Fale podatci', 400

    with db.engine.connect() as connection:
        connection.execute(text("""INSERT INTO Opazaji (ID_voca, slikaPI, KlasaModel, Vrijeme) 
                                VALUES (:ID_voca, :slikaPI , :KlasaModel, :Vrijeme);"""),
                           ID_voca=ID_voca, slikaPI=slikaPI, KlasaModel=KlasaModel,
                           Vrijeme=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        connection.execute(text("""UPDATE Voce SET TrenutnaKlasa = :KlasaModel WHERE ID = :ID_voca;"""),
                           ID_voca=ID_voca, KlasaModel=KlasaModel,)

    return 'Upisano: ' + datetime.now().strftime("%H:%M:%S")


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(join(main.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@main.route('/api/model', methods=['POST'])
def model():
    data = request.json
    slikaPI = data['slikaPI']
    pic = transform(image=asarray(Image.open(BytesIO(b64decode(slikaPI)))))
    result = evaluation(modelML, pic["image"])
    result = int(result.numpy()[0])+1
    return str(result)

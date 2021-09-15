# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 21:36:53 2021

@author: Mislav
"""
import os
import PIL
import torch
import albumentations
import numpy as np
import torchvision

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
from base64 import b64encode, b64decode
from sqlalchemy.sql import text
from datetime import datetime
from PIL import Image
from io import BytesIO
from albumentations.pytorch import ToTensorV2


app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "Secret Key"

os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://mislav1:MojPass123456@iot-2021-mislavspajic-server.database.windows.net/iot-2021-mislavspajic-db?driver=ODBC+Driver+17+for+SQL+Server"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#ML model

transform = albumentations.Compose([
    albumentations.SmallestMaxSize(224), 
    albumentations.CenterCrop(224, 224),
    albumentations.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2()
    ])
    
modelML = torch.load(os.getcwd()+'/model/final_model.pth',map_location='cpu')
   
def evaluation(model,image):
    model.eval()
    image=image.unsqueeze_(0)
    with torch.no_grad():
        ps = torch.exp(model.forward(image))
        _, predTest = torch.max(ps,1) 
    return predTest



# Voce Class/Model


class Voce(db.Model):

    ID = db.Column(db.Integer, primary_key=True)
    Ime = db.Column(db.VARCHAR(50))
    slika = db.Column(db.VARBINARY(None))
    BeaconUUID = db.Column(db.VARCHAR(100))
    BeaconMajor = db.Column(db.Integer)
    BeaconMinor = db.Column(db.Integer)
    OsnovnaCijena = db.Column(db.Float)
    TrenutnaKlasa = db.Column(db.Integer)
    popusti = db.relationship('Opazaji', lazy=True)
    opazaji = db.relationship('Popusti', lazy=True)

    def __init__(self, Ime, slika, BeaconUUID, BeaconMajor, BeaconMinor, OsnovnaCijena, TrenutnaKlasa):
        self.Ime = Ime
        self.slika = slika
        self.BeaconUUID = BeaconUUID
        self.BeaconMajor = BeaconMajor
        self.BeaconMinor = BeaconMinor
        self.OsnovnaCijena = OsnovnaCijena
        self.TrenutnaKlasa = TrenutnaKlasa

# Popusti Class/Model


class Popusti(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ID_voce = db.Column(db.Integer, db.ForeignKey(('voce.ID')), nullable=False)
    Ime_Klase = db.Column(db.VARCHAR(50))
    Klasa = db.Column(db.Integer)
    Popust = db.Column(db.Float)

    def __init__(self, ID_voce, Ime_Klase, Klasa, Popust):
        self.ID_voce = ID_voce
        self.Ime_Klase = Ime_Klase
        self.Klasa = Klasa
        self.Popust = Popust

# Opazaji Class/Model


class Opazaji(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ID_voca = db.Column(db.Integer, db.ForeignKey(('voce.ID')), nullable=False)
    slikaPI = db.Column(db.VARBINARY(None))
    KlasaModel = db.Column(db.Integer)
    Vrijeme = db.Column(db.DATETIME)

    def __init__(self, ID_voca, slikaPI, KlasaModel, Vrijeme):
        self.ID_voca = ID_voca
        self.slikaPI = slikaPI
        self.KlasaModel = KlasaModel
        self.Vrijeme = Vrijeme


@app.route('/', methods=['GET'])
def Index():
    all_data = Voce.query.all()
    for row in all_data:
        row.slika = row.slika.decode('ascii')

    return render_template("index.html", voca=all_data)

@app.route('/discounts', methods=['GET'])
def Discounts():
    all_data = Popusti.query.all()

    return render_template("discounts.html", popusti=all_data)

@app.route('/observations', methods=['GET'])
def Observations():
    all_data = Opazaji.query.all()
    for row in all_data:
        row.slikaPI = row.slikaPI.decode('ascii')

    return render_template("observations.html", opazaji=all_data)

# New Fruit
@app.route('/voce/insert', methods=['POST'])
def add_voce():
    if request.method == 'POST':
        Ime = request.form['Ime']
        slika = request.files['slika']
        BeaconUUID = request.form['BeaconUUID']
        BeaconMajor = request.form['BeaconMajor']
        BeaconMinor = request.form['BeaconMinor']
        OsnovnaCijena = request.form['OsnovnaCijena']
        TrenutnaKlasa = request.form['TrenutnaKlasa']
        slika.save(os.path.join(app.instance_path, 'htmlfi',
                   secure_filename(slika.filename)))
        with open(os.path.join(app.instance_path, 'htmlfi', slika.filename), 'rb') as imagefile:
            slika2 = b64encode(imagefile.read())

        novo_voce = Voce(Ime, slika2, BeaconUUID, BeaconMajor,
                         BeaconMinor, OsnovnaCijena, TrenutnaKlasa)
        db.session.add(novo_voce)
        try:db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('Index'))

        flash("Fruit Inserted Successfully")

        return redirect(url_for('Index'))

# Update Fruit
@app.route('/voce/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Voce.query.get(request.form.get('ID'))
        my_data.Ime = request.form['Ime']
        my_data.BeaconUUID = request.form['BeaconUUID']
        my_data.BeaconMajor = request.form['BeaconMajor']
        my_data.BeaconMinor = request.form['BeaconMinor']
        my_data.OsnovnaCijena = request.form['OsnovnaCijena']
        my_data.TrenutnaKlasa = request.form['TrenutnaKlasa']
        if request.files['slika'].filename != '':
            my_data.slika = request.files['slika']
            my_data.slika.save(os.path.join(
                app.instance_path, 'htmlfi', secure_filename(my_data.slika.filename)))
            with open(os.path.join(app.instance_path, 'htmlfi', my_data.slika.filename), 'rb') as imagefile:
                my_data.slika = b64encode(imagefile.read())

        try:db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('Index'))
        flash("Fruit Updated Successfully")

        return redirect(url_for('Index'))

# Delete Fruit
@app.route('/voce/delete/<ID>', methods=['GET', 'POST'])
def delete(ID):
    my_data = Voce.query.get(ID)
    db.session.delete(my_data)
    try:db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash(error)
        return redirect(url_for('Index'))
    flash("Fruit Deleted Successfully")

    return redirect(url_for('Index'))

# New Discount
@app.route('/discount/insert', methods=['POST'])
def add_popust():
    if request.method == 'POST':
        ID_voce = request.form['ID_voce']
        Ime_Klase = request.form['Ime_Klase']
        Klasa = request.form['Klasa']
        Popust = request.form['Popust']
  
        novi_popust = Popusti(ID_voce, Ime_Klase, Klasa, Popust)
        db.session.add(novi_popust)
        try:db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('Discounts'))
        
        flash("Discount Inserted Successfully")

        return redirect(url_for('Discounts'))
    
# Update Discount
@app.route('/discount/update', methods=['GET', 'POST'])
def update_disc():
    if request.method == 'POST':
        my_data = Popusti.query.get(request.form.get('ID'))
        my_data.ID_voce = request.form['ID_voce']
        my_data.Ime_Klase = request.form['Ime_Klase']
        my_data.Klasa = request.form['Klasa']
        my_data.Popust = request.form['Popust']
        try:db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('Discounts'))
        flash("Discount Updated Successfully")

        return redirect(url_for('Discounts'))

# Delete Discount
@app.route('/discount/delete/<ID>', methods=['GET', 'POST'])
def delete_disc(ID):
    my_data = Popusti.query.get(ID)
    db.session.delete(my_data)
    try:db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash(error)
    flash("Discount Deleted Successfully")

    return redirect(url_for('Discounts'))

# New Observation
@app.route('/observation/insert', methods=['POST'])
def add_opazaj():
    if request.method == 'POST':
        ID_voca = request.form['ID_voca']
        slikaPI = request.files['slikaPI']
        KlasaModel = request.form['KlasaModel']
        Vrijeme = request.form['Vrijeme'].replace("T"," ")
        slikaPI.save(os.path.join(app.instance_path, 'htmlfi',
                   secure_filename(slikaPI.filename)))
        with open(os.path.join(app.instance_path, 'htmlfi', slikaPI.filename), 'rb') as imagefile:
            slikaPI2 = b64encode(imagefile.read())

        novi_opazaj = Opazaji(ID_voca, slikaPI2, KlasaModel, Vrijeme)
        db.session.add(novi_opazaj)
        try:db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('Observations'))
        flash("Observation Inserted Successfully")

        return redirect(url_for('Observations'))

# Update Observation
@app.route('/observation/update', methods=['GET', 'POST'])
def update_obs():
    if request.method == 'POST':
        my_data = Opazaji.query.get(request.form.get('ID'))
        my_data.ID_voca = request.form['ID_voca']
        my_data.KlasaModel = request.form['KlasaModel']
        my_data.Vrijeme = request.form['Vrijeme'].replace("T"," ")
        if request.files['slikaPI'].filename != '':
            my_data.slikaPI = request.files['slikaPI']
            my_data.slikaPI.save(os.path.join(
                app.instance_path, 'htmlfi', secure_filename(my_data.slikaPI.filename)))
            with open(os.path.join(app.instance_path, 'htmlfi', my_data.slikaPI.filename), 'rb') as imagefile:
                my_data.slikaPI = b64encode(imagefile.read())

        try:db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
            return redirect(url_for('Observations'))
        flash("Observation Updated Successfully")

        return redirect(url_for('Observations'))

# Delete Observation
@app.route('/observation/delete/<ID>', methods=['GET', 'POST'])
def delete_obs(ID):
    my_data = Opazaji.query.get(ID)
    db.session.delete(my_data)
    try:db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash(error)
        return redirect(url_for('Observations'))
    flash("Observation Deleted Successfully")

    return redirect(url_for('Observations'))

### Send UUID and back info
@app.route('/api/beacon',methods=['GET'])
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
        result_dict = [{column: value for column, value in row.items()} for row in result]
        result_dict[0]["Popust"]=str(result_dict[0]["Popust"])
        result_dict[0]["OsnovnaCijena"]=str(result_dict[0]["OsnovnaCijena"])
        
        if result_dict:
            return result_dict[0]
        else:
            return 'No fruit assigned to this Beacon UUID, Major and Minor combination'
        
@app.route('/api/uploadPI',methods=['POST'])
def uploadPI():
    data=request.json
    if 'ID_voca' and 'slikaPI' and 'KlasaModel' in data:
        ID_voca = str(data['ID_voca'])
        slikaPI = str(data['slikaPI'])
        slikaPI = bytes(slikaPI,'ascii')
        KlasaModel = str(data['KlasaModel'])
    else:
        return 'Fale podatci', 400

    with db.engine.connect() as connection:
        connection.execute(text("""INSERT INTO Opazaji (ID_voca, slikaPI, KlasaModel, Vrijeme) 
                                VALUES (:ID_voca, :slikaPI , :KlasaModel, :Vrijeme);"""),
                                ID_voca=ID_voca,slikaPI=slikaPI,KlasaModel=KlasaModel,
                                Vrijeme=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        connection.execute(text("""UPDATE Voce SET TrenutnaKlasa = :KlasaModel WHERE ID = :ID_voca;"""),
                                ID_voca=ID_voca,KlasaModel=KlasaModel,)  
   
   

    return 'Upisano: ' + datetime.now().strftime("%H:%M:%S")
    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/model', methods=['POST'])
def model():
    data=request.json
    slikaPI = data['slikaPI']
    pic=transform(image=np.asarray(PIL.Image.open(BytesIO(b64decode(slikaPI)))))
    result=evaluation(modelML,pic["image"])
    result=int(result.numpy()[0])+1
    return str(result)
      
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

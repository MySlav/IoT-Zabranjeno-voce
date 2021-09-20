# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 21:08:38 2021

@author: Mislav
"""

from . import db
from flask_login import UserMixin


# Fruit Class/Model


class Voce(db.Model):

    ID = db.Column(db.Integer, primary_key=True)
    Ime = db.Column(db.VARCHAR(50))
    slika = db.Column(db.VARCHAR(None))
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

# Discounts Class/Model


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

# Observations Class/Model


class Opazaji(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ID_voca = db.Column(db.Integer, db.ForeignKey(('voce.ID')), nullable=False)
    slikaPI = db.Column(db.VARCHAR(None))
    KlasaModel = db.Column(db.Integer)
    Vrijeme = db.Column(db.DATETIME)

    def __init__(self, ID_voca, slikaPI, KlasaModel, Vrijeme):
        self.ID_voca = ID_voca
        self.slikaPI = slikaPI
        self.KlasaModel = KlasaModel
        self.Vrijeme = Vrijeme
        
# User Class/Model


class Users(UserMixin,db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Password = db.Column(db.VARCHAR(100))
    Name = db.Column(db.VARCHAR(100), unique=True)
    
    def __init__(self, ID, password, name):
        self.password = password
        self.name = name
        
    def get_id(self):
           return (self.ID)


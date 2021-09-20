# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 13:26:57 2021

@author: Mislav
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import Users
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(Name=username).first()

        # check if the user actually exists
        # take the user-supplied pass, hash it, and compare it to hashed pass
        if not user or not check_password_hash(user.Password, password):
            flash('Please check your login details and try again.')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('auth.login'))

        # if the above check passes, then we know the user has the right creds
        login_user(user, remember=remember)
        return redirect(url_for('main.Index'))

    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

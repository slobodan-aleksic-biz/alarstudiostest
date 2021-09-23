import os

from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify, flash
import asyncio

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.sql import text


from init import app

from models import User, bcrypt, db

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])


@app.before_request
def before_request():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        g.user = user
    else:
        g.user = None


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('users'))
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    g.user = None
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    session.pop('user_id', None)

    username = request.form['username']
    password = request.form['password']

    if username == '' or password == '':
        return jsonify({'action': 0, 'message': 'The username and password fields are mandatory!'})

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({'action': 1})

    return jsonify({'action': 0, 'message': 'You cannot login! Check your credentials!'})


@app.route('/users')
def users():
    if 'user_id' not in session:
        return redirect('/')

    users = User.query.all()

    return render_template('users.html', users=users)


def defaultRequests():

    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    is_admin = True if request.form['is_admin'] == '1' else False

    return [name, username, password, is_admin]


@app.route('/users/store', methods=['POST'])
def store_user():
    if request.method == 'POST':

        [name, username, password, is_admin] = defaultRequests()

        if name == '' or username == '' or password == '':
            return jsonify({'action': 0, 'message': 'Mandatory fields are required!'})

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return jsonify({'action': 0, 'message': 'The user with the username already exists!'})

        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        user = User(name=name, username=username,
                    password=hashed_password, is_admin=is_admin)
        db.session.add(user)

        db.session.commit()

    next_number = User.query.count()

    return jsonify({'action': 1, 'message': 'User is created!', 'id': user.id, 'name': user.name, 'username': user.username, 'is_admin': user.is_admin, 'next_number': next_number})


@app.route('/users/<int:id>/edit', methods=['GET'])
def edit_user(id):
    if g.user.is_admin == False:
        return jsonify({'action': 0, 'message': 'You do not have permission to delete the user!'})

    user = User.query.filter_by(id=id).first()
    if user == None:
        flash('The user is not found!')

    return render_template('edit_user.html', user=user)


@app.route('/users/<int:id>/modify', methods=['POST'])
def modify_user(id):
    if g.user.is_admin == False:
        return jsonify({'action': 0, 'message': 'You do not have permission to delete the user!'})

    user = User.query.filter_by(id=id).first()
    if user == None:
        return jsonify({'action': 0, 'message': 'The user is not found!'})

    [name, username, password, is_admin] = defaultRequests()

    if name == '' or username == '':
        return jsonify({'action': 0, 'message': 'Mandatory fields are required!'})

    if username != user.username:
        userExists = User.query.filter_by(username=username).first()
        if userExists:
            return jsonify({'action': 0, 'message': 'The user with the username already exists!'})

    try:
        user.name = name
        user.username = username
        if password:
            user.password = bcrypt.generate_password_hash(
                password).decode('utf-8')
        user.is_admin = is_admin
        # db.session.flush()
        db.session.commit()
        return jsonify({'action': 1, 'message': 'User is modified!'})
    except:
        return jsonify({'action': 0, 'message': 'Error!'})


@app.route('/users/<int:id>/delete', methods=['GET'])
def delete_user(id):
    if g.user.is_admin == False:
        return jsonify({'action': 0, 'message': 'You do not have permission to delete the user!'})

    user = User.query.filter_by(id=id).first()
    if user == None:
        flash('The user is not found!')
    else:
        db.session.delete(user)

        db.session.commit()

    return redirect('/')



''' Second task (async calls) '''
def feedSources(n, m):
    l = list()
    d = dict()
    for i in range(n, n+10):
        l.append({"id": str(i), "name": "Test "+str(i)})
    for i in range(m, m+10):
        l.append({"id": str(i), "name": "Test "+str(i)})

    return l


@app.route('/source_a', methods=['GET'])
def source_a():
    l = feedSources(1, 31)
    return jsonify(results=l, status=200)


@app.route('/source_b', methods=['GET'])
def source_b():
    l = feedSources(11, 41)
    return jsonify(results=l, status=200)


@app.route('/source_c', methods=['GET'])
def source_c():
    l = feedSources(21, 51)
    return jsonify(results=l, status=200)

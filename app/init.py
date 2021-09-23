import os

from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify, flash
import asyncio
from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'asdfad12ed12d13de'

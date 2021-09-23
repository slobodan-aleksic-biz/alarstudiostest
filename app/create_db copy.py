import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from models import bcrypt

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])

with engine.connect() as con:
    hashed_password = bcrypt.generate_password_hash('secret').decode('utf-8')
    data = (
        {"id": 1, "name": "Slobodan", "username": "slobodan",
            "password": hashed_password, "is_admin": True},
        {"id": 1, "name": "Slobodan 2", "username": "slobodan1",
            "password": hashed_password, "is_admin": True},
        {"id": 1, "name": "Slobodan 3", "username": "Slobodan2",
            "password": hashed_password, "is_admin": True},
    )

    statement = text(
        """INSERT INTO users(id, name, username, password, is_admin) VALUES(:id, :name, :username, :password, :is_admin)""")

    for line in data:
        con.execute(statement, **line)

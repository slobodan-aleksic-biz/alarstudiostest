from models import User, bcrypt,db

db.drop_all()
db.create_all()

hashed_password = bcrypt.generate_password_hash('secret').decode('utf-8')
user = User(name='slobodan', username='slobodan', password=hashed_password, is_admin=True)

db.session.add(user)
db.session.commit()


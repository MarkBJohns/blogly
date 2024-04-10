from models import User, db
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()

    User.query.delete()

    user_1 = User(first_name='John', last_name='Doe')

    db.session.add(user_1)

    db.session.commit()


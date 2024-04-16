from models import User, Post, db
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()

    User.query.delete()
    Post.query.delete()

    user_1 = User(first_name='John', last_name='Doe')

    post_1 = Post(
        title='This is a post',
        content='I am writing this post in order to have sample data',
        user=user_1
    )

    db.session.add(user_1)
    db.session.add(post_1)

    db.session.commit()


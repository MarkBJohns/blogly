"""Blogly application."""

from flask import Flask, render_template, request, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, default_profile_img

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.debug = True
app.config['SECRET_KEY'] = 'blogly'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

connect_db(app)
with app.app_context():
    db.create_all()

initialized = False

@app.route('/')
def home():
    return redirect(url_for('show_users'))

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form['first_name']
        print(first_name)
        last_name = request.form['last_name']
        print(last_name)
        image_url = request.form['picture'] or default_profile_img
        print(image_url)

        user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        print(user)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('show_users'))
    
    return render_template('signup.html')

@app.route('/users/<int:user_id>')
def show_profile(user_id):
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['picture'] or default_profile_img
        db.session.commit()
        return redirect(url_for('show_profile', user_id=user.id))
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    if not initialized:
        with app.app_context():
            db.create_all()
        initialized = True
    app.run()



from unittest import TestCase

from app import app
from models import db, User, Post, default_profile_img

second_default = 'https://imgs.search.brave.com/WzsJxrd95PAh6aWhwpATikTtTAnHJl_xX00Luqxvp_U/rs:fit:860:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzAzLzQwLzEyLzQ5/LzM2MF9GXzM0MDEy/NDkzNF9iejNwUVRM/cmRGcEg5MmVra251/YVRIeThKdVhnRzdm/aS5qcGc'


class UserTestCase(TestCase):
    """Testing users table"""

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        app.config['TESTING'] = True
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            user = User(first_name="Test", last_name="User", image_url=default_profile_img)
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_show_users(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_sign_up(self):
        response = self.client.post('/users/new', data=dict(
            first_name='Test',
            last_name='User',
            picture=default_profile_img
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            user = User.query.filter_by(first_name='Test').first()
            self.assertIsNotNone(user)

    def test_show_profile(self):
        response = self.client.get(f'/users/{self.user_id}')
        self.assertEqual(response.status_code, 200)

class PostTestCase(TestCase):
    """Testing posts table"""

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        app.config['TESTING'] = True
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            user = User(first_name='Test', last_name='User', image_url=default_profile_img)
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id

            post = Post(title='Test Post', content='This is a test post', user_id=self.user_id)
            db.session.add(post)
            db.session.commit()
            self.post_id = post.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_show_post(self):
        response = self.client.get(f'/posts/{self.post_id}')
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post(f'/users/{self.user_id}/posts/new', data=dict(
            title='New Test Post',
            content='This is a new test post'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            post = Post.query.filter_by(title='New Test Post').first()
            self.assertIsNotNone(post)

    def test_edit_post(self):
        response = self.client.post(f'/posts/{self.post_id}/edit', data=dict(
            title='Edited Test Post',
            content='This is an edited test post'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            post = Post.query.get(self.post_id)
            self.assertEqual(post.title, 'Edited Test Post')
            self.assertEqual(post.content, 'This is an edited test post')

    def test_delete_post(self):
        response = self.client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            post = Post.query.get(self.post_id)
            self.assertIsNone(post)
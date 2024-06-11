import unittest
from app import app, db, User
from werkzeug.security import generate_password_hash

class HealthYouAuthTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True
        
        # Create the database and the database tables
        db.create_all()

        # Create a test user
        hashed_password = generate_password_hash('testpassword', method='sha256')
        self.test_user = User(name='Test User', username='testuser', email='test@example.com',
                              password=hashed_password, birthday='1990-01-01', sex='M')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        # Remove the database tables and the database
        db.session.remove()
        db.drop_all()

    def signup(self, name, username, email, password, password_verify, birthday, sex):
        return self.app.post('/signup', data=dict(
            name=name,
            username=username,
            email=email,
            password=password,
            passwordVerify=password_verify,
            birthday=birthday,
            sex=sex
        ), follow_redirects=True)

    def login(self, login_identity, password):
        return self.app.post('/login', data=dict(
            login_identity=login_identity,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.post('/logout', follow_redirects=True)

    # Sign-Up Tests
    def test_successful_signup(self):
        response = self.signup('New User', 'newuser', 'new@example.com', 'newpassword', 'newpassword', '1991-01-01', 'F')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created successfully!', response.data)

    def test_signup_password_mismatch(self):
        response = self.signup('New User', 'newuser', 'new@example.com', 'newpassword', 'wrongpassword', '1991-01-01', 'F')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Passwords do not match!', response.data)

    def test_signup_existing_user(self):
        response = self.signup('Test User', 'testuser', 'test@example.com', 'testpassword', 'testpassword', '1990-01-01', 'M')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Email or Username already exists!', response.data)

    def test_signup_missing_data(self):
        response = self.signup('', 'newuser', 'new@example.com', 'newpassword', 'newpassword', '1991-01-01', 'F')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Missing data', response.data)

    # Login Tests
    def test_successful_login(self):
        response = self.login('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_login_invalid_credentials(self):
        response = self.login('wronguser', 'wrongpassword')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid credentials!', response.data)

    def test_login_empty_username(self):
        response = self.login('', 'testpassword')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Missing data', response.data)

    def test_login_empty_password(self):
        response = self.login('testuser', '')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Missing data', response.data)

    def test_logout(self):
        self.login('testuser', 'testpassword')
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged out successfully!', response.data)

if __name__ == '__main__':
    unittest.main()
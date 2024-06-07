import unittest
from app import app, mongo
import mongomock

class HealthYouTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mongo_patch = mongomock.patch(servers=(('localhost', 27017),))
        cls.mongo_patch.start()
        cls.app = app.test_client()
        cls.app.testing = True

    @classmethod
    def tearDownClass(cls):
        cls.mongo_patch.stop()

    def setUp(self):
        self.db = mongomock.MongoClient().healthyou
        mongo.db = self.db

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn(b'HealthYou', rv.data)

    def test_signup(self):
        rv = self.app.post('/signup', data=dict(
            name='Test User',
            email='test@example.com',
            password='password',
            passwordVerify='password',
            birthday='1990-01-01',
            sex='male'
        ), follow_redirects=True)
        self.assertIn(b'Account created successfully!', rv.data)
        user = self.db.users.find_one({'email': 'test@example.com'})
        self.assertIsNotNone(user)

    def test_signup_password_mismatch(self):
        rv = self.app.post('/signup', data=dict(
            name='Test User',
            email='test@example.com',
            password='password',
            passwordVerify='password123',
            birthday='1990-01-01',
            sex='male'
        ), follow_redirects=True)
        self.assertIn(b'Passwords do not match!', rv.data)

    def test_login(self):
        self.db.users.insert_one({
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password',
            'birthday': '1990-01-01',
            'sex': 'male'
        })
        rv = self.app.post('/login', data=dict(
            email='test@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertIn(b'Login successful!', rv.data)

    def test_invalid_login(self):
        rv = self.app.post('/login', data=dict(
            email='nonexistent@example.com',
            password='password'
        ), follow_redirects=True)
        self.assertIn(b'Invalid credentials!', rv.data)

    def test_set_reminder(self):
        rv = self.app.post('/set_reminder', data=dict(
            reminder_type='hydration',
            interval='2hourly'
        ), follow_redirects=True)
        self.assertIn(b'Reminder set successfully!', rv.data)
        reminder = self.db.reminders.find_one({'reminder_type': 'hydration'})
        self.assertIsNotNone(reminder)

    def test_contact(self):
        rv = self.app.post('/contact', data=dict(
            contactName='Test User',
            contactEmail='test@example.com',
            contactMessage='This is a test message.'
        ), follow_redirects=True)
        self.assertIn(b'Message sent successfully!', rv.data)
        contact = self.db.contacts.find_one({'email': 'test@example.com'})
        self.assertIsNotNone(contact)

if __name__ == '__main__':
    unittest.main()
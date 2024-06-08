import unittest
from app import app, db, User, Reminder, Contact

class HealthYouTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.app.post('/signup', data=dict(
            name='Test User',
            email='test@example.com',
            password='password123',
            passwordVerify='password123',
            birthday='01-01-2000',
            sex='male'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created successfully!', response.data)

        # Verify user in database
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)

    def test_login(self):
        self.app.post('/signup', data=dict(
            name='Test User',
            email='test@example.com',
            password='password123',
            passwordVerify='password123',
            birthday='01-01-2000',
            sex='male'
        ))
        response = self.app.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_set_reminder(self):
        self.app.post('/signup', data=dict(
            name='Test User',
            email='test@example.com',
            password='password123',
            passwordVerify='password123',
            birthday='01-01-2000',
            sex='male'
        ))
        self.app.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ))
        response = self.app.post('/set_reminder', data=dict(
            **{
                'reminder-type': 'Hydration',
                'interval': '2hourly'
            }
        ))
        print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reminder set successfully!', response.data)

        # Verify reminder in database
        reminder = Reminder.query.filter_by(reminder_type='Hydration').first()
        self.assertIsNotNone(reminder)

    def test_get_reminders(self):
        self.app.post('/signup', data=dict(
            name='Test User',
            email='test@example.com',
            password='password123',
            passwordVerify='password123',
            birthday='01-01-2000',
            sex='male'
        ))
        self.app.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ))
        self.app.post('/set_reminder')
        
        response = self.app.post('/set_reminder', data=dict(
            **{
                'reminder-type': 'Hydration',
                'interval': '2hourly'
            }
        ))
        response = self.app.get('/get_reminders')
        print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hydration', response.data)

    def test_delete_reminder(self):
        self.app.post('/signup', data=dict(
            name='Test User',
            email='test@example.com',
            password='password123',
            passwordVerify='password123',
            birthday='01-01-2000',
            sex='male'
        ))
        self.app.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ))
        self.app.post('/set_reminder', data=dict(
            **{
                'reminder-type': 'Hydration',
                'interval': '2hourly'
            }
        ))
        reminder = Reminder.query.first()
        if reminder:  # Check if reminder exists before trying to delete
            response = self.app.delete(f'/delete_reminder/{reminder.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Reminder deleted successfully!', response.data)
        else:
            self.fail('Reminder was not created successfully.')

    def test_contact(self):
        response = self.app.post('/contact', data=dict(
            contactName='Test User',
            contactEmail='test@example.com',
            contactMessage='This is a test message.'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Message sent successfully!', response.data)

        # Verify contact in database
        contact = Contact.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(contact)

    def test_logout(self):
        self.app.post('/signup', data=dict(
            name='Test User',
            email='test@example.com',
            password='password123',
            passwordVerify='password123',
            birthday='01-01-2000',
            sex='male'
        ))
        self.app.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ))
        response = self.app.post('/logout')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged out successfully!', response.data)

if __name__ == '__main__':
    unittest.main()
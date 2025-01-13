from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        self.register_data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        self.login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

    def test_can_register(self):
        """Users can register with valid credentials"""
        response = self.client.post(reverse('register'), data=self.register_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.data['message'], 'User registered successfully')
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')
    
    def test_cannot_register_with_missing_fields(self):
        """Users cannot register with missing fields"""
        response = self.client.post(reverse('register'), data={}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Please provide username, password, and email')
    
    def test_cannot_register_with_existing_username(self):
        """Users cannot register with an existing username"""
        data = {
            'username': 'testuser',
            'password': 'newpassword',
            'email': 'newuser@example.com'
        }
        response = self.client.post(reverse('register'), data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Username already exists')
    
    def test_cannot_register_with_existing_email(self):
        """Users cannot register with an existing email"""
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'testuser@example.com'
        }
        response = self.client.post(reverse('register'), data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Email already exists')

    def test_can_login(self):
        """Users can login with valid credentials"""
        response = self.client.post(reverse('login'), data=self.login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Login successful')
        self.assertEqual(response.data['user']['username'], 'testuser')
        self.assertEqual(response.data['user']['email'], 'testuser@example.com')

    def test_cannot_login_with_invalid_credentials(self):
        """Users cannot login with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Invalid credentials')

    def test_can_logout(self):
        """Users can logout"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('logout'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Logout successful')

    def test_can_get_csrf_token(self):
        """Users can get a CSRF token"""
        response = self.client.get(reverse('get_csrf_token'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('csrfToken' in response.data)

    def test_can_get_user_info_when_authenticated(self):
        """Users can get their user info when authenticated"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('get_user_info'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_cannot_get_user_info_when_not_authenticated(self):
        """Users cannot get their user info when not authenticated"""
        response = self.client.get(reverse('get_user_info'), format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .forms import UserSignUpForm

# Create your tests here.

class UserSignUpFormTest(TestCase):
    """Test cases for UserSignUpForm"""
    
    def test_form_has_email_field(self):
        """Test that the form includes the email field"""
        form = UserSignUpForm()
        self.assertIn('email', form.fields)
        self.assertEqual(form.fields['email'].label, 'Email Address')
        self.assertTrue(form.fields['email'].required)
    
    def test_form_fields_order(self):
        """Test that the form fields are in the correct order"""
        form = UserSignUpForm()
        expected_fields = ['username', 'email', 'password1', 'password2']
        self.assertEqual(list(form.fields.keys()), expected_fields)
    
    def test_form_validation_with_valid_data(self):
        """Test form validation with valid data"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_validation_without_email(self):
        """Test form validation without email"""
        form_data = {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_form_validation_with_duplicate_email(self):
        """Test form validation with duplicate email"""
        # Create a user with the email first
        User.objects.create_user(
            username='existinguser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Try to create another user with the same email
        form_data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_form_validation_with_invalid_email(self):
        """Test form validation with invalid email format"""
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_form_save_creates_user_with_email(self):
        """Test that form.save() creates a user with the email"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

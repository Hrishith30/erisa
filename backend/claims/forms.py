from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserSignUpForm(UserCreationForm):
    """Custom signup form with username, email, password, and confirm password"""
    
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        }),
        help_text='We\'ll use this email for important notifications and account recovery.',
        required=True
    )
    
    # Override the default password fields to use custom labels
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        help_text='Your password must contain at least 8 characters.'
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        help_text='Enter the same password as before, for verification.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the username field
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['username'].help_text = ''
        
    def clean_username(self):
        """Validate that username is unique and valid"""
        username = self.cleaned_data.get('username')
        
        # First check if username is provided
        if not username:
            raise ValidationError("Username is required.")
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        
        return username
        
    def clean_email(self):
        """Validate that email is unique and valid"""
        email = self.cleaned_data.get('email')
        
        # First check if email is provided
        if not email:
            raise ValidationError("Email address is required.")
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email address already exists.")
        
        return email
        
    def clean_password2(self):
        """Validate that both passwords match"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        # Only validate password2 if password1 is provided
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        
        return password2
        


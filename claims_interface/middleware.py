from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for dashboard URLs
        if request.path.startswith('/dashboard/'):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                # Redirect to login page
                return redirect('login')
        
        response = self.get_response(request)
        return response

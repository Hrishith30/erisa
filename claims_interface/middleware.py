from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip middleware for login, logout, and static files
        if (request.path.startswith('/login/') or 
            request.path.startswith('/logout/') or 
            request.path.startswith('/static/') or
            request.path == '/'):
            response = self.get_response(request)
            return response
        
        # Check if the request is for dashboard URLs
        if request.path.startswith('/dashboard/'):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                # Redirect to login page
                return redirect('login')
        
        # Also check for admin URLs
        if request.path.startswith('/admin/'):
            # Check if user is authenticated and is staff
            if not request.user.is_authenticated or not request.user.is_staff:
                # Redirect to login page
                return redirect('login')
        
        response = self.get_response(request)
        return response

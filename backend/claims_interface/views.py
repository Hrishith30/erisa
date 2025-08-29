from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import os

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'healthy', 
        'message': 'Claims Management System is running',
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'database': settings.DATABASES['default']['ENGINE']
    })

def debug_info(request):
    """Debug information endpoint"""
    info = {
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'database_engine': settings.DATABASES['default']['ENGINE'],
        'static_url': settings.STATIC_URL,
        'static_root': str(settings.STATIC_ROOT),
        'secret_key_set': bool(settings.SECRET_KEY and settings.SECRET_KEY != 'django-insecure-your-secret-key-here'),
        'environment_vars': {
            'DATABASE_URL': bool(os.getenv('DATABASE_URL')),
            'SECRET_KEY': bool(os.getenv('SECRET_KEY')),
            'DEBUG': os.getenv('DEBUG'),
            'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS'),
        }
    }
    return JsonResponse(info)

def handler404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)

def handler500(request):
    """Custom 500 error handler"""
    return render(request, '500.html', status=500)

def handler403(request, exception):
    """Custom 403 error handler"""
    return render(request, '403.html', status=403)

def handler400(request, exception):
    """Custom 400 error handler"""
    return render(request, '400.html', status=400)

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os

def health_check(request):
    """Simple health check endpoint"""
    return HttpResponse("OK", content_type="text/plain")

def root_view(request):
    """Root view that redirects to appropriate page"""
    try:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard/')
        else:
            return HttpResponseRedirect('/login/')
    except Exception as e:
        # Fallback to login page if there's any error
        return HttpResponseRedirect('/login/')

def handler404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)

def handler500(request):
    """Custom 500 error handler"""
    return render(request, '500.html', status=500)

def handler403(request, exception):
    """Custom 403 error handler"""
    return render(request, '404.html', status=403)

def handler400(request, exception):
    """Custom 400 error handler"""
    return render(request, '404.html', status=400)

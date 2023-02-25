from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.



def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def read(request):
    return render(request, 'security.html')


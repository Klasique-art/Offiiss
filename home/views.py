from django.shortcuts import render

# Create your views here.



def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

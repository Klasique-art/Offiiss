from django.shortcuts import render

# Create your views here.

def home_page(request):
    msg = None
    if request.session.get('visit'):
        msg = True
    else:
        msg = False
        request.session['visit'] = 'visit'
    return render(request, 'home/index.html', {'msg': msg})

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

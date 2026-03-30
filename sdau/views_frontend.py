from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden  # ✅ AJOUT
from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect('sdau:carte')
    return redirect('sdau:login')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('sdau:carte')
    return render(request, 'sdau/login.html')

def register_page(request):
    if request.user.is_authenticated:
        return redirect('sdau:carte')
    return render(request, 'sdau/register.html')

@login_required(login_url='/login/')
def carte(request):
    return render(request, 'sdau/carte.html')

@login_required(login_url='/login/')
def administration_view(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Accès refusé")
    return render(request, 'sdau/administration.html')
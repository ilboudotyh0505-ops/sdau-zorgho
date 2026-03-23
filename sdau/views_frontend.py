"""
Vues pour les pages frontend
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def index(request):
    """Page d'accueil - redirige vers carte si connecté"""
    if request.user.is_authenticated:
        return redirect('sdau:carte')
    return redirect('sdau:login')


def login_page(request):
    """Page de connexion"""
    if request.user.is_authenticated:
        return redirect('sdau:carte')
    return render(request, 'sdau/login.html')


def register_page(request):
    """Page d'inscription"""
    if request.user.is_authenticated:
        return redirect('sdau:carte')
    return render(request, 'sdau/register.html')


@login_required(login_url='/login/')
def carte(request):
    """Page principale de la carte"""
    return render(request, 'sdau/carte.html')

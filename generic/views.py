from django.shortcuts import render
from generic.forms import ProductForm

# Create your views here.


def base(request):
    return render(request, 'index.html')


def homepage(request):
    return render(request, 'home.html')


def legal(request):
    return render(request, 'legal.html')

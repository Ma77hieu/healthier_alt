from django.shortcuts import render
from generic.forms import ProductForm

# Create your views here.


def base(request):
    # form = ProductForm()
    # return render(request, 'index.html', {'form': form})
    return render(request, 'index.html')


def homepage(request):
    # form = ProductForm()
    # return render(request, 'home.html', {'form': form})
    return render(request, 'home.html')


def legal(request):
    return render(request, 'legal.html')

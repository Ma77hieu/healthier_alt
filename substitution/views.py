from django.shortcuts import render
from substitution.models import Product


def results(request):
    products = Product.objects.all()
    return render(request, 'results.html', {'products': products})


def details(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'detailprod.html', {'product': product})

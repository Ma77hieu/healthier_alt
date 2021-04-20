from django.shortcuts import render
from substitution.models import Product, Favorites


def results(request):
    products = Product.objects.all()
    return render(request, 'results.html', {'products': products})


def details(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'detailprod.html', {'product': product})


def favorites(request, user):
    user_favs = Favorites.objects.filter(user_id=user)
    favs_ids_list = []
    for fav in user_favs:
        favs_ids_list.append(fav.product_id)
    user_fav_prod = Product.objects.filter(pk__in=favs_ids_list)
    # user_fav_prod = Product.objects.get(pk=2)
    return render(request, 'favorites.html', {'fav_products': user_fav_prod})

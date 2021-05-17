from django.shortcuts import render
from substitution.models import Product, Favorites
from django.core.paginator import Paginator
from .constants import NBR_RESULTS_PER_PAGE as per_page


def results(request):
    products = Product.objects.all().order_by(
        'product_name').distinct('product_name')
    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    searched_product = request.GET.get('searched_product')
    return render(request, 'results.html', {
        'products': products,
        'searched_product': searched_product,
        'page_obj': page_obj})


def details(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'detailprod.html', {'product': product})


def favorites(request, user):
    user_favs = Favorites.objects.filter(user_id=user)
    # favs_ids_list = []
    # for fav in user_favs:
    #     favs_ids_list.append(fav.product_id)
    # user_fav_prod = Product.objects.filter(pk__in=favs_ids_list)
    # user_fav_prod = Product.objects.get(pk=2)
    return render(request, 'favorites.html', {'fav_products': user_favs})

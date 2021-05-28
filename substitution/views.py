from django.shortcuts import render
from substitution.models import Product, Favorites
from django.core.paginator import Paginator
from .constants import NBR_RESULTS_PER_PAGE as per_page
from substitution.search_engine import Substitutes


# def results_all(request):
#     """Kept for now for testing purposes
#     returns all products for any search"""
#     products = Product.objects.all().order_by(
#         'product_name').distinct('product_name')
#     paginator = Paginator(products, per_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     searched_product = request.GET.get('searched_product')
#     return render(request, 'results.html', {
#         'products': products,
#         'searched_product': searched_product,
#         'page_obj': page_obj})


def results(request):
    """uses the search engine to find a matching product and 
    the alternatives, returns paginated results"""
    searched_product = request.GET.get('searched_product')
    print("SEARCHED PROD: {}".format(searched_product))
    alt = Substitutes()
    alt_products_ids = alt.find_alt(searched_product)[0]
    print("PRODUCTS ID: {}".format(alt_products_ids))
    search_match_product_id = alt.searched_product_id
    search_match_product = Product.objects.get(pk=search_match_product_id)
    print("SEARCH_MATCH_PRODUCT: {}".format(search_match_product))
    print("SEARCH_MATCH_PRODUCT IMAGE: {}".format(
        search_match_product.image_front_small_url))
    products = Product.objects.filter(pk__in=alt_products_ids)
    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'results.html', {
        'products': products,
        'searched_product': searched_product,
        'search_match_product': search_match_product,
        'page_obj': page_obj})


def details(request, product_id):
    """access a specific product details page based on product id"""
    product = Product.objects.get(pk=product_id)
    return render(request, 'detailprod.html', {'product': product})


def favorites(request, logged_user_id):
    """access the saved favorites of a user based on logged user id"""
    user_favs = Favorites.objects.filter(user_id=logged_user_id)
    # favs_ids_list = []
    # for fav in user_favs:
    #     favs_ids_list.append(fav.product_id)
    # user_fav_prod = Product.objects.filter(pk__in=favs_ids_list)
    # user_fav_prod = Product.objects.get(pk=2)
    return render(request, 'favorites.html', {'fav_products': user_favs})


# def add_favorites(request, current_user_id, fav_product_id):
#     fav = Favorites(product_id=fav_product_id,
#                     user_id=current_user_id)
#     fav.save()
#     paginator = Paginator(products, per_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     searched_product = request.GET.get('searched_product')
#     return render(request, 'results.html', {
#         'products': products,
#         'searched_product': searched_product,
#         'page_obj': page_obj})

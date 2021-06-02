from django.shortcuts import render
from substitution.models import Product, Favorites
from django.core.paginator import Paginator
from .constants import NBR_RESULTS_PER_PAGE as per_page
from .constants import NOT_LOGGED_IN, NO_PROD_FOUND
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
    # print("user_id: {}".format(request.user.id))
    fav_saved = False

    if request.user.id:
        fav_product_id = request.GET.get('fav_prod')
        if fav_product_id:
            fav = Favorites(product_id=fav_product_id,
                            user_id=request.user.id)
            fav.save()
            fav_saved = True
    print("fav_saved: {}".format(fav_saved))
    searched_product = request.GET.get('searched_product')
    print("SEARCHED PROD: {}".format(searched_product))
    alt = Substitutes()
    if alt.find_alt(searched_product):
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
            'page_obj': page_obj,
            'fav_saved': fav_saved})
    else:
        error = NO_PROD_FOUND
        return render(request, 'home.html', {'error': error})


def details(request, product_id):
    """access a specific product details page based on product id"""
    product = Product.objects.get(pk=product_id)
    return render(request, 'detailprod.html', {'product': product})


def mesaliments(request):
    """access the saved favorites of a user based on logged user id"""
    if request.user.id:
        favorites = Favorites.objects.filter(
            user_id=request.user.id).values('product_id')
        # print("FAVORITES OF THE USER: {}".format(favorites))
        favs = []
        for favorite in favorites:
            # print("FAVORITE: {}".format(favorite))
            # print("FAVORITE PRODUCT ID: {}".format(favorite["product_id"]))
            favs.append(favorite["product_id"])

        # print("IDs FAVORITES OF THE USER: {}".format(favs))
        products = Product.objects.filter(pk__in=favs)
        paginator = Paginator(products, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        favoritepage = True
        return render(request, 'results.html', {
            'products': products,
            'page_obj': page_obj,
            'is_favorite_page': favoritepage})

    else:
        error = NOT_LOGGED_IN
        return render(request, 'home.html', {'error': error})

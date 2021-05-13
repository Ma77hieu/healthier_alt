from django.urls import path
from substitution import views

urlpatterns = [
    path('results', views.results, name="results"),
    path('details/<int:product_id>', views.details, name="details"),
    path('user/<int:user>/favorites', views.favorites, name="favorites"),
]

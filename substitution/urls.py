from django.urls import path
from substitution import views

urlpatterns = [
    path('results', views.results, name="results"),
    path('<int:product_id>/details', views.details, name="details")
]

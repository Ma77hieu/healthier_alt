from django.urls import path
from substitution import views

urlpatterns = [
    path('results', views.results, name="results"),
    path('details', views.details, name="details")
]

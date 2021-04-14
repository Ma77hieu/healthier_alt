from django.urls import path
from authentification import views

urlpatterns = [
    path('signin', views.signin, name="signin"),
    path('user', views.user, name="user")
]

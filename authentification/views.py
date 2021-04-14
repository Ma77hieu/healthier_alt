from django.shortcuts import render

# Create your views here.


def signin(request):
    return render(request, 'signin.html')


def user(request):
    return render(request, 'user.html')

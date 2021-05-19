from django.shortcuts import render, redirect
# from authentification.models import User
from authentification.forms import UserForm
from authentification.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def login_user(request, user_name, pwd, signup):
    auth = authenticate(username=user_name,
                        password=pwd)
    print("AUTH:{}".format(auth))
    if auth is not None:
        logged_user = login(request, auth)
        if signup == True:
            html_page = 'signin.html'
        else:
            html_page = 'user.html'
        return render(request, html_page, {
            'form': logged_user})
    else:
        print(
            request, "Unsuccessful registration. Invalid Credentials.")
        messages.error(
            request, "Unsuccessful registration. Invalid Credentials.")


def signup(request):
    if request.method == "GET":
        form = UserForm()
    elif request.method == "POST":
        print("----\nSIGNUP\n----")
        print("REQUEST.POST:{}".format(request.POST))
        # print("request username:{}".format(request.POST["username"]))
        # print("request password:{}".format(request.POST["password"]))

        form = UserForm(request.POST)
        if form.is_valid():
            print('form: {}'.format(form))
            form.save()
            # print('PASSWORD AUTH:{}'.format(form.cleaned_data['password']))
            user_name = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            signup = True
            login_user(request, user_name, pwd, signup)

        else:
            messages.error(
                request, "Unsuccessful registration. Invalid information.")

    return render(request, 'signin.html', {'form': form})


def signin(request):
    if request.method == "GET":
        form = UserForm()
    elif request.method == "POST":
        print("----\nSIGNIN\n----")
        print("REQUEST.POST:{}".format(request.POST))
        # print("request username:{}".format(request.POST["username"]))
        # print("request password:{}".format(request.POST["password"]))
        user_name = request.POST['username']
        pwd = request.POST['password']
        signup = False
        login_user(request, user_name, pwd, signup)
    form = UserForm()
    return render(request, 'signin.html', {'form': form})


def logout_user(request):
    logout(request)
    print("user logged out")
    return render(request, 'home.html')


def user(request):
    return render(request, 'user.html')

from django.shortcuts import render, redirect
from authentification.forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from substitution.constants import LOG_IN_OK, LOG_OUT_OK, INVALID_CREDENTIALS


# Create your views here.

def login_user(request, user_name, pwd, signup):
    print(user_name)
    print(pwd)

    auth = authenticate(request, username=user_name,
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
        print(INVALID_CREDENTIALS)
        return INVALID_CREDENTIALS
        # print(
        #     request, "Unsuccessful registration. Invalid Credentials.")
        # messages.error(
        #     request, "Unsuccessful registration. Invalid Credentials.")


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
            form_update = form.save(commit=False)
            form_update.password = make_password(form.cleaned_data['password'])
            form_update.save()
            user_name = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            signup = True
            login_user(request, user_name, pwd, signup)

        else:
            messages.error(
                request, "Unsuccessful registration. Invalid information.")
            signup = False

    return render(request, 'signin.html', {'form': form, 'signup': signup})


def signin(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, 'signin.html', {'form': form})
    elif request.method == "POST":
        print("----\nSIGNIN\n----")
        print("REQUEST.POST:{}".format(request.POST))
        # print("request username:{}".format(request.POST["username"]))
        # print("request password:{}".format(request.POST["password"]))
        user_name = request.POST['username']
        pwd = request.POST['password']
        signup = False
        login = login_user(request, user_name, pwd, signup)
        if login == INVALID_CREDENTIALS:
            form = UserForm()
            return render(request, 'signin.html', {'form': form, 'error': INVALID_CREDENTIALS})
        else:
            return render(request, 'home.html', {'user_message': LOG_IN_OK})


def logout_user(request):
    print("REQUEST.USER: {}".format(request.user))
    logout(request)
    print("user logged out")
    print("REQUEST.USER: {}".format(request.user))
    user_message = LOG_OUT_OK
    return render(request, 'home.html', {'user_message': user_message})


def user(request):
    return render(request, 'user.html')

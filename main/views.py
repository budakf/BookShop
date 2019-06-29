from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template import RequestContext
from django.conf.urls import handler404


from django.contrib.auth.models import User
from .registrationForm import RegistrationForm
from.loginForm import LoginForm

# Create your views here.

def homePage(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                messages.error(request, f"Username already exists")
                return render(request, "register.html", {'form': form,})

            if User.objects.filter(email=form.cleaned_data["email"]).exists():
                messages.error(request, f"Email already exists")
                return render(request, "register.html",{'form':form})

            if form.cleaned_data["password"] != form.cleaned_data["re_password"]:
                messages.error(request, f"Passwords do not match")
                return render(request, "register.html",{'form':form})

            user = User.objects.create_user(
                form.cleaned_data["username"],
                form.cleaned_data["email"],
                form.cleaned_data["password"],
            )
            user.first_name = form.cleaned_data["first_name"] 
            user.last_name = form.cleaned_data["last_name"] 
            user.save() 
            messages.success(request, f"New User Created")
            messages.success(request, f"Lets Login")
            return redirect("/login")

    elif request.user.is_authenticated:
        return redirect("/")

    else:
        form = RegistrationForm()
        return render(request=request,template_name="register.html",context={"form":form})


def login_request(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,f"Login as {username} Succesfully")
                return redirect("/")
            else:
                messages.error(request,f"Username or Password Wrong")
                return redirect("/login",{'form':form})
    
    elif request.user.is_authenticated:
        messages.info(request, f"You have already logged in")
        return redirect("/")

    else:
        print(request.GET)
        form = LoginForm()
        return render(request=request,template_name="login.html",context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, f"Logout Succesfully")
    return redirect("/")

def about(request):
    return render(request, "about.html")


def handler404(request):
    print("sfbfdsb")
    response = render_to_response('404.html', {},
                              context_instance=RequestContext(request))
    response.status_code = 404
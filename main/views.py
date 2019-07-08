from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template import RequestContext
from django.conf.urls import handler404

from django.contrib.auth.models import User
from .registrationForm import RegistrationForm
from .loginForm import LoginForm
from .models import Book, Cart, Customer

# Create your views here.

def homePage(request):
    books = Book.objects.all()
    return render(request, "home.html",{"books":books})


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
            customer = Customer()
            customer.user = user
            customer.save()
            messages.success(request, f"New User Created")
            messages.success(request, f"Lets Login")
            return redirect("/login")

    elif request.user.is_authenticated:
        return redirect("/")

    else:
        form = RegistrationForm()
        return render(request=request,template_name="register.html",context={"form":form})


def login_request(request):
    if request.user.is_authenticated:
        messages.info(request, f"You have already logged in")
        return redirect("/")
        
    elif request.method == "POST":
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
    response = render_to_response('404.html', {},
                              context_instance=RequestContext(request))
    response.status_code = 404


def cart(request):
    try:
        cart = Cart.objects.get(owner__username=request.user)
    except:
        cart = None
    
    total_fee = 0
    if cart is not None:
        books = cart.books.all()
        for book in books:
            total_fee += book.book_price
        
    return render( request, "cart.html", {"cart": cart , "total_fee": total_fee} )


def add_book_to_cart(request):
    if request.method == "POST":
        request_data = request.POST
        book_name = request_data.get("book_name")
        try:
            cart = Cart.objects.get(owner__username=request.user)
        except:
            cart = None
        if cart is not None:
            try:   
                book = Book.objects.get(book_name=book_name)
            except:    
                book = None
            if book is not None:
                cart.books.add(book) 
                messages.info(request, f"{book.book_name} added to cart")
    
        return redirect('homePage')

    else:
        return redirect('notFound')


def delete_book_from_cart(request):
    if request.method == "POST":
        request_data = request.POST
        book_name = request_data.get("book_name")

        cart = Cart.objects.filter(owner__username=request.user)[0]
        book = Book.objects.filter(book_name=book_name)[0]
        cart.books.remove(book)
        
        books = cart.books.all()
        total_fee = 0
        for b in books:
            total_fee += b.book_price

        messages.info(request, f"{book.book_name} removed from cart")
        return redirect("/cart")  

    else:
        return redirect("/notFound")        


def account(request):
    try:
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user__username=user)
    except:
        account = None
            
    return render(request, "account.html", {"customer": customer} )


def edit_email(request):

    if request.method == "POST":
        new_email = request.POST.get("new_email")
        if new_email == request.user.email:
            messages.error(request, f"Please enter new email")
        elif User.objects.filter(email=new_email).exists():
            messages.error(request, f"Email already exists")

        else:
            user = User.objects.get(username=request.user)
            user.email = new_email
            user.save()
            messages.success(request, f"Edited email successfully")
        
        return redirect("/account")
 
    else:
        account = User.objects.filter(username=request.user)[0]
        edit = True
        return render(request, "account.html", {"account": account, "edit_email": edit})

def edit_phone(request):
    if request.method == "POST":
        new_phone = request.POST.get("new_phone")
        customer = Customer.objects.get(user__username=request.user)
        if new_phone == customer.phone:
            messages.error(request, f"Please new phone")
        else:
            customer.phone = new_phone
            customer.save()
            messages.success(request, f"Edited phone successfully")

        return redirect("/account")
    
    else:
        account = Customer.objects.get(user__username=request.user)
        edit = True
        return render(request, "account.html", {"account": account, "edit_phone": edit})
            

def edit_address(request):
    if request.method == "POST":
        new_address = request.POST.get("new_address")
        customer = Customer.objects.get(user__username=request.user)
        if new_address == customer.address:
            messages.error(request, f"Please new address")
        else:
            customer.address = new_address
            customer.save()
            messages.success(request, f"Edited address successfully")

        return redirect("/account")
    
    else:
        account = Customer.objects.get(user__username=request.user)
        edit = True
        return render(request, "account.html", {"account": account, "edit_address": edit})
      
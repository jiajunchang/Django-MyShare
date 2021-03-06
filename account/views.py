from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import MyUserCreationForm
from .models import Contact
from image.models import Image

'''
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .forms import LoginForm

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd["username"],
                password=cd["password"]
            )
            if user != None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated Successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
        return render(
            request,
            "account/login.html",
            {"form": form}
        )
'''
@login_required
def home(request):
    image_list = []
    
    for user in request.user.following.all():
        for image in Image.objects.filter(user=user):
            image_list.append(image)
    image_list.sort(key=lambda x: x.created, reverse=True)

    paginator = Paginator(image_list, 3)
    page = request.GET.get("page")
    try:
        image_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        image_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        image_list = paginator.page(paginator.num_pages)

    return render(
        request,
        "account/home.html",
        {"images": image_list}
    )

def register(request):
    if request.method == "POST":
        user_form = MyUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data["password1"]
            )
            new_user.save()
            return render(
                request,
                "account/register_done.html",
                {"new_user": new_user}
            )
    else:
        user_form = MyUserCreationForm()
    return render(
        request,
        "account/register.html",
        {"user_form": user_form}
    )

@login_required
def profile(request, username):
    user = User.objects.filter(username=username).first()
    return render(
        request,
        "account/profile.html",
        {"user": user}
    )

@login_required
def user_list(request):
    user_list = User.objects.all()
    return render(
        request,
        "account/user_list.html",
        {"user_list": user_list}
    )

@login_required
def follow(request, username):
    user_to = User.objects.filter(username=username).first()
    user_from = request.user
    con = Contact(
        user_from = user_from,
        user_to = user_to
    )
    con.save()
    return redirect("user_page", id=user_to.id)

@login_required
def unfollow(request, username):
    user_to = User.objects.filter(username=username).first()
    user_from = request.user
    con = Contact.objects.filter(user_from = user_from, user_to = user_to).first()
    if con:
        con.delete()
    return redirect("user_page", id=user_to.id)

@login_required
def user_page(request, id):
    user = User.objects.filter(id=id).first()
    image_list = Image.objects.filter(user=user)
    paginator = Paginator(image_list, 12)
    page = request.GET.get("page")
    try:
        image_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        image_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        image_list = paginator.page(paginator.num_pages)

    return render(
        request,
        "account/user_page.html",
        {
            "user": user,
            "images": image_list
        }
    )

@login_required
def following_users(request, id):
    user = User.objects.filter(id=id).first()
    following_users = user.following.all()
    return render(
        request,
        "account/following_users.html",
        {"following_users": following_users}
    )

@login_required
def follower_users(request, id):
    user = User.objects.filter(id=id).first()
    followers = user.followers.all()
    return render(
        request,
        "account/follower_users.html",
        {"followers": followers}
    )
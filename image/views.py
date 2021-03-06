from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.contrib.auth.models import User

from .forms import ImageForm, CommentForm, TagForm
from .models import Image, Comment
from account.models import Contact

@login_required
def image_upload(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            return render(request, "image/image_upload_done.html")
    else:
        form = ImageForm()
    return render(
        request,
        "image/image_upload.html",
        {"form": form}
    )

@login_required
def image_list(request, tag_slug=None):
    if tag_slug:
        tag = Tag.objects.filter(slug=tag_slug).first()
        image_list = Image.objects.filter(tags__in=[tag])
    else:
        image_list = Image.objects.all()
    
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
        "image/image_list.html",
        {"images": image_list}
    )

@login_required
def image_detail(request, id, slug):
    image = Image.objects.filter(id=id, slug=slug).first()

    # List of active comments
    comments = image.comment.filter(active=True)
    new_comment = None
    if request.method == "POST":
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.image = image
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        "image/image_detail.html",
        {
            "image": image,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form
        }
    )

@login_required
def image_like(request, id):
    image = Image.objects.get(id=id)
    image.user_like.add(request.user)
    return redirect("image_app:image_detail", id=id, slug=image.slug)

@login_required
def image_unlike(request, id):
    image = Image.objects.get(id=id)
    image.user_like.remove(request.user)
    return redirect("image_app:image_detail", id=id, slug=image.slug)

@login_required
def add_tag(request, id):
    image = Image.objects.get(id=id)

    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            for tag in tags.split(','):
                image.tags.add(tag)
            return redirect("image_app:image_detail", id=id, slug=image.slug)
    else:
        form = TagForm()
    return render(
        request,
        "image/add_tag.html",
        {"tag_form": form}
    )

@login_required
def image_follow(request, id):
    image = Image.objects.get(id=id)
    user_to = User.objects.filter(username=image.user.username).first()
    user_from = request.user
    con = Contact(
        user_from = user_from,
        user_to = user_to
    )
    con.save()
    return redirect("image_app:image_detail", id=id, slug=image.slug)

@login_required
def image_unfollow(request, id):
    image = Image.objects.get(id=id)
    user_to = User.objects.filter(username=image.user.username).first()
    user_from = request.user
    con = Contact.objects.filter(user_from = user_from, user_to = user_to).first()
    if con:
        con.delete()
    return redirect("image_app:image_detail", id=id, slug=image.slug)
from django.contrib import admin
from .models import Image, Comment

# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "user", "created")
    list_filter = ("user", "created")
    search_fields = ("title", "description")
    ordering = ("user", "created")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "image", "created", "active")
    list_filter = ("active", "created", "user")
    search_fields = ("user", )
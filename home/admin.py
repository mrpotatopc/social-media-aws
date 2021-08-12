from django.contrib import admin
from . import models
# Register your models here.

from .models import post, post_image, post_video

class post_imageAdmin(admin.StackedInline):
    model = post_image

class post_videoAdmin(admin.StackedInline):
    model = post_video

@admin.register(post)
class postAdmin(admin.ModelAdmin):
    inlines = [post_imageAdmin, post_videoAdmin]

    class Meta:
       model = post

@admin.register(post_image)
class post_imageAdmin(admin.ModelAdmin):
    pass

@admin.register(post_video)
class post_videoAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.subscription)
admin.site.register(models.post_comment)
admin.site.register(models.user_image)
admin.site.register(models.user_name)

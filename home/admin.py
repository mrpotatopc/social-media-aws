from django.contrib import admin
from . import models
# Register your models here.

from .models import post, post_image, post_video,user_premium,post_attached_link,reply

class post_imageAdmin(admin.StackedInline):
    model = post_image

class post_videoAdmin(admin.StackedInline):
    model = post_video

class post_attached_linkAdmin(admin.StackedInline):
    model = post_attached_link

@admin.register(post)
class postAdmin(admin.ModelAdmin):
    inlines = [post_imageAdmin, post_videoAdmin, post_attached_linkAdmin]

    class Meta:
       model = post

@admin.register(post_image)
class post_imageAdmin(admin.ModelAdmin):
    pass

@admin.register(post_video)
class post_videoAdmin(admin.ModelAdmin):
    pass

@admin.register(post_attached_link)
class post_attached_linkAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.subscription)
admin.site.register(models.post_comment)
admin.site.register(models.user_image)
admin.site.register(models.user_name)
admin.site.register(models.user_premium)
admin.site.register(models.reply)
admin.site.register(models.report_reason)
admin.site.register(models.report)

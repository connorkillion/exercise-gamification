from django.contrib import admin
from .models import Exercise, Profile, City, Post
from .models import InstagramAccount, Publication, Tag

# Use this link to assist in implementing Instagram component https://github.com/dannywillems/django-instagram


class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


class PublicationAdmin(admin.ModelAdmin):
    list_display = ("image_tag", "instagram_account_id", "publish_at")


class InstagramAccountAdmin(admin.ModelAdmin):
    list_display = ("username", "password")


admin.site.register(InstagramAccount, InstagramAccountAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Exercise)
admin.site.register(Profile)
admin.site.register(City)
admin.site.register(Post)


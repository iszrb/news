from django.contrib import admin
from app.models import *



class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter =['name']

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["username", "gender", "mobile", "email", "is_staff", "is_superuser"]
    search_fields = ["username", "gender", "mobile", "email"]
    list_filter = ["username", "gender", "mobile", "email"]
    list_editable = ["is_staff", "is_superuser"]
    ordering = ["id"]

class ContentAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "picture"]
    search_fields = ["id", "publish_time", "title", "picture"]
    ordering = ["-publish_time"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "user_id", "news_id", "state"]
    search_fields = ["id", "publish_time", "user_id", "news_id"]
    list_editable = ["state"]
    ordering = ["-publish_time"]


admin.site.register(Type, TypeAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Comment, CommentAdmin)


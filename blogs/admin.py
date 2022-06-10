from django.contrib import admin
from django.shortcuts import render,redirect
from .models import *

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
  

# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('Name',)}

admin.site.register(Group,BlogAdmin)
admin.site.register(Post)
admin.site.register(GroupJoined)
# admin.site.register(BlogAuthor)
admin.site.register(BlogReply)
admin.site.register(PostComment)
# admin.site.register(Category,CategoryAdmin)
# admin.site.register(Subscribe)

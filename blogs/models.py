from tokenize import group
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField 
from ckeditor.fields import RichTextField
class Group(models.Model):
    author      =       models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title       =       models.CharField(max_length=1000)
    slug        =       models.CharField(max_length=1000)
    image       =       models.ImageField(blank=True)
    description =       RichTextUploadingField()
    created_at  =       models.DateTimeField(auto_now_add=True)
    updated     =       models.DateTimeField(auto_now=True)
    publish     =       models.BooleanField(blank=True,default=False)
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
class GroupJoined(models.Model):
    joined_group= models.ForeignKey(Group, on_delete=models.CASCADE) 
    joined_by= models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.group.title
class Post(models.Model):
    group       =       models.ForeignKey(Group, on_delete= models.CASCADE)
    post_by     =       models.ForeignKey(User, on_delete=models.CASCADE)
    post_text   =       RichTextField(blank= True, null = True) 
    # post_text   =       models.CharField(max_length=500, default='') 
    post_created=       models.DateTimeField(auto_now_add= True)
    def __str__(self):
        return self.group.title

class PostComment(models.Model):
    name        =       models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email       =       models.CharField(max_length=100)
    description =       RichTextField(blank= True, null = True)
    # description =       models.TextField(max_length=1000)
    post_date   =       models.DateTimeField(auto_now_add=True)
    blog        =       models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return self.description
    
  



class BlogReply(models.Model):
    name        =       models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email       =       models.CharField(max_length=100)
    description =       models.TextField(max_length=1000)
    post_date   =       models.DateTimeField(auto_now_add=True)
    comment     =       models.ForeignKey(PostComment, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return self.name


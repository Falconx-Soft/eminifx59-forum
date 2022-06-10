from operator import mod
from tokenize import group
from turtle import title
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
        return self.joined_group.title

class Post(models.Model):
    group       =       models.ForeignKey(Group, on_delete= models.CASCADE)
    post_by     =       models.ForeignKey(User, on_delete=models.CASCADE)
    title       =       models.CharField(max_length=1000, null=True)
    post_text   =       RichTextField(blank= True, null = True)
    post_created=       models.DateTimeField(auto_now_add= True)
    def __str__(self):
        return self.title

class PostComment(models.Model):
    name        =       models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description =       models.TextField(blank= True, null = True)
    post_date   =       models.DateTimeField(auto_now_add=True)
    post        =       models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return str(self.id)
    
  



class CommentReply(models.Model):
    name        =       models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description =       models.TextField(max_length=1000)
    post_date   =       models.DateTimeField(auto_now_add=True)
    comment     =       models.ForeignKey(PostComment, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return str(self.comment.id)

class Profile(models.Model):
    user            =       models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_image   =       models.ImageField()

    def __str__(self):
        return str(self.user.username)
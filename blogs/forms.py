from lib2to3.pgen2 import grammar
from django import forms
from django.forms import ModelForm
from .models import *
from ckeditor.widgets import CKEditorWidget
class Comment(ModelForm):
    
    class Meta:
        model = PostComment
        fields =  [
            'name',     
            'email',       
            'description',         
             
    
        ]

class Reply(ModelForm):
    class Meta:
        model = BlogReply
        fields =  [
            'name',     
            'email',       
            'description',         
]




class blogform(ModelForm):
    class Meta:
        model=Group
        exclude = ['author','slug','publish']
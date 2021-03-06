from multiprocessing import context
import pstats
from tokenize import group
from turtle import title
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import slugify
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method== 'POST':
        fullname= request.POST.get('name')
        username= request.POST.get('username')
        email= request.POST.get('email')
        password= request.POST.get('password')
        if User.objects.filter(email=email):
            return redirect(request, 'signup.html')
        user_obj= User(username=username, email=email, first_name= fullname) 
        user_obj.set_password(password)
        user_obj.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        
        return redirect('list')	
    return render(request, 'home.html')

@login_required(login_url="")
def create_group(request):
    if request.method== 'POST':
        title = request.POST.get('title')
        slug = title.replace(" ","-")
        description= request.POST.get('description')
        gropu_obj= Group.objects.create(author=request.user,slug=slug, title= title , description= description)
        gropu_obj.save()
        return redirect('list')	
    return render(request, 'home.html')


def loginUser(request):
        if request.user.is_authenticated:
            return redirect('list')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.get(username=username)
            if user:
                username = user.username
                user = authenticate(request, username=username, password=password) # check password

            if user is not None:
                login(request, user)
                return redirect('list')	
            
        return render(request,'home.html',)

def logoutUser(request):
        logout(request)
        return redirect('/')

@login_required(login_url="")
def create_post(request):
    if request.method== 'POST':
        post_text= request.POST.get('post_text')
        slug= request.POST.get('slug')
        group_obj = Group.objects.get(slug=slug)
        title = request.POST.get('title')
        post_obj= Post.objects.create(group = group_obj, post_by=request.user, title=title, post_text= post_text )
        post_obj.save()

        return redirect(reverse('detail', args = [slug]))
    return render(request,'home.html')

@login_required(login_url="")
def create_comment(request):
   
    if request.method== 'POST':

        id = request.POST.get('id')
        post_obj = Post.objects.get(id=id)
        description= request.POST.get('comment')
        comment_obj= PostComment.objects.create(name = request.user, description= description, post =  post_obj)
        comment_obj.save()

        return redirect(reverse('post',args=[id]))
    return render(request,'home.html')

@login_required(login_url="")
def create_reply(request):
   
    if request.method== 'POST':
        comment_id= request.POST.get('id')
        description= request.POST.get('comment')
        post_id = request.POST.get('post_id')
        
        comment_obj = PostComment.objects.get(id=comment_id)
        comment_obj= CommentReply.objects.create(name = request.user, description= description, comment = comment_obj )
        comment_obj.save()

        return redirect(reverse('post', args = [post_id]))
    return render(request,'home.html')

@login_required(login_url="")
def join_group(request,id):
    
    Group_obj = Group.objects.get(slug=id)
    GroupJoined_obj = GroupJoined.objects.create(joined_group=Group_obj, joined_by=request.user)
    GroupJoined_obj.save()

    return redirect(reverse('detail', args = [id]))

def GroupList(request):
    groups = Group.objects.all()
    resent_groups = Group.objects.all()[:4]
    count = groups.count()

    paginator = Paginator(groups ,10) # Shows only 10 records per page

    page = request.GET.get('page')
    try:
        group = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        group = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 7777), deliver last page of results.
        group = paginator.page(paginator.num_pages)
        
    for i in (group):
        i.description=i.description[:500]
    context = {
        'groups':groups,
        'group':group,
        'count':count,
        'resent_groups':resent_groups
    }
    return render(request,'grouplist.html',context)


def GroupDetail(request,slug):
    resent_groups = Group.objects.all()[:4]
    group = Group.objects.get(slug=slug)
    posts= Post.objects.filter(group=group)
    temp = False

    for g in GroupJoined.objects.filter(joined_group=group):
        if g.joined_by == request.user:
            temp = True
    context = {
        'group':group,
        'posts':posts,
        'is_member':temp,
        'resent_groups':resent_groups
    }
    return render(request,'groupdetail.html',context)

@login_required(login_url="")
def GroupMembers(request, slug):
    group = Group.objects.get(slug=slug)
    resent_groups = Group.objects.all()[:4]
    members = GroupJoined.objects.filter(joined_group=group)
    context = {
        'group':group,
        'members':members,
        'resent_groups':resent_groups
    }
    return render(request,'groupmembers.html',context)

def ViewPost(request,id):
    post_obj = Post.objects.get(id=id)
    post_comment = PostComment.objects.filter(post=post_obj)

    resent_groups = Group.objects.all()[:4]

    context = {
        'post':post_obj,
        'comments':post_comment,
        'resent_groups':resent_groups
    }
    return render(request,'post.html',context)

@login_required(login_url="")
def view_profile(request,id):
    user_obj = User.objects.get(id=id)

    resent_groups = Group.objects.all()[:4]
    context = {
        'user_obj':user_obj,
        'resent_groups':resent_groups
    }
    return render(request, 'profile.html',context)

@login_required(login_url="")
def user_post(request,id):
    user_obj = User.objects.get(id=id)
    posts = Post.objects.filter(post_by=user_obj)
    resent_groups = Group.objects.all()[:4]

    context = {
        'user_obj':user_obj,
        'posts':posts,
        'resent_groups':resent_groups
    }
    return render(request, 'user_post.html',context)

def home(request):
    resent_groups = Group.objects.all()[:4]
    context = {
        'resent_groups':resent_groups
    }
    return render(request,'home.html',context)

def store_email(request):
    if request.method== 'POST':
        e = request.POST.get('email')
        email_obj = email.objects.create(email=e)
        email_obj.save()
        return redirect('home')
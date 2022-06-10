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
        
        return redirect('/bloglist')
    return render(request, 'register.html')

def create_group(request):
    username= request.user.username
    user_obj= User.objects.filter(username= username)
    if request.method== 'POST':
        title= request.POST.get('title')
        slug= title.replace(" ","-")
        print(slug)
        description= request.POST.get('description')
        gropu_obj= Group.objects.create(author=user_obj[0],slug= slug, title= title , description= description)

        return redirect('/bloglist')
    return render(request, 'create_group.html')


def loginUser(request):
        if request.user.is_authenticated:
            return redirect('/bloglist')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.get(username=username)
            if user:
                username = user.username
                user = authenticate(request, username=username, password=password) # check password

            if user is not None:
                login(request, user)
                return redirect('/bloglist')	
            
        return render(request,'login.html',)

def logoutUser(request):
        print('1212122')
        logout(request)
        return redirect('/')

def create_post(request):
    print('___________________________')
    username= request.user.username
    user_obj= User.objects.filter(username= username)
   
    if request.method== 'POST':
        post_text= request.POST.get('post_text')
        slug= request.POST.get('slug')
        group_obj = Group.objects.get(slug=slug)
        print('___________________________')
        print('post_text', post_text)
        post_obj= Post.objects.create(group = group_obj, post_by=user_obj[0], post_text= post_text )
        post_obj.save()

        return redirect(reverse('detail', args = [slug]))
    return render(request,'blogdetail.html')

def create_comment(request):
    print('___________________________')
    username= request.user.username
    user_obj= User.objects.filter(username= username)
   
    if request.method== 'POST':
        post_id= request.POST.get('post_id')
        name= request.POST.get('name')
        email= request.POST.get('email')
        description= request.POST.get('description')
        slug= request.POST.get('slug')
        post_obj = Post.objects.get(id=post_id)
        
        comment_obj= PostComment.objects.create(name = name, email=email, description= description, blog = post_obj )
        comment_obj.save()

        return redirect(reverse('detail', args = [slug]))
    return render(request,'blogdetail.html')

def create_reply(request):
    print('___________________________')
    username= request.user.username
    user_obj= User.objects.filter(username= username)
   
    if request.method== 'POST':
        comment_id= request.POST.get('comment_id')
        name= request.POST.get('name')
        email= request.POST.get('email')
        description= request.POST.get('description')
        slug= request.POST.get('slug')
        comment_obj = PostComment.objects.get(id=comment_id)
        
        comment_obj= BlogReply.objects.create(name = name, email=email, description= description, comment = comment_obj )
        comment_obj.save()

        return redirect(reverse('detail', args = [slug]))
    return render(request,'blogdetail.html')

def join_group(request):
    username= request.user.username
    user_obj= User.objects.get(username=username)
    if request.method== 'POST':
        group = request.POST.get('group_id')
        group_obj= Group.objects.get(id=group)
        join_group_obj= GroupJoined.objects.create(joined_group= group_obj, joined_by= user_obj)
        join_group_obj.save()
        slug= request.POST.get('slug')
        return redirect(reverse('detail', args = [slug]))
    return render(request,'blogdetail.html')

def BlogList(request):
    groups = Group.objects.all()

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
        'group':group
    }
    return render(request,'bloglist.html',context)

def BlogDetail(request,slug):
    lis   = Group.objects.all()
    group = Group.objects.get(slug=slug)
    
    posts= Post.objects.filter(group=group)
    # comments= PostComment.objects.filter(blog=posts[0])
    # reply = BlogReply.objects.filter(comment = comments)    
    # print(reply)
    replies = BlogReply.objects.all()
    # print(comments)
    form = Comment()
    form_1 = Reply()
    if request.method =='POST':
         form=Comment(request.POST or None)
         if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.blog=group
            new_comment.save()
            form.save()
            return HttpResponseRedirect(reverse('detail', args=[slug]))
             
 
    context = {
        'blogs':group,
        
        'posts':posts,
        'list':lis,
        'form':form,
        # 'relpy' : reply,
        'replies' : replies,
        'form_1' : form_1,
    }
    return render(request,'blogdetail.html',context)

def home(request):
    return render(request,'home.html')
from django.conf.urls import url
from . import views
from django.urls import path,include


urlpatterns = [

    url(r'grouplist',views.GroupList,name='list'),
    url(r'^detail/(?P<slug>[-\w]+)$',views.GroupDetail,name='detail'),

    url(r'^members/(?P<slug>[-\w]+)$',views.GroupMembers, name="members"),

    path('post/<int:id>/',views.ViewPost, name="post"),

    path('profile/<int:id>', views.view_profile, name="profile"),

    path('user_post/<int:id>', views.user_post, name="user_post"),

    path('', views.home, name="home"),

    url('register',views.register,name='register'),
    url('logout', views.logoutUser, name="logout"),
    url('comment', views.create_comment, name="comment"),
    url('reply', views.create_reply, name="reply"),
    path('join_group/<str:id>', views.join_group, name="join_group"),
    
    url('creategroup',views.create_group,name="create_group"),
    url('postcreate', views.create_post, name="postcreate"),
    url('login/', views.loginUser, name="login"),
    
    
    


####################################################################################################



    # url(r'^authorlist/',views.BlogAuthors,name='authorlist'),    
    # url(r'^author/(?P<id>\d+)$', views.BlogListByAuthor, name="blog-by-author"),
    # # url(r'^category/(?P<slug>[-\w]+)/$', views.base, name='category'),
    # # url(r'^cat/', views.base1, name='cat'),
    # # url(r'^subscribe/',views.sub,name='subscribe'),
    # # url(r'^contact/',views.Contact,name='contact'),


]
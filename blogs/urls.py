from django.conf.urls import url
from . import views
from django.urls import path,include


urlpatterns = [

    url(r'bloglist',views.BlogList,name='list'),
    url(r'^detail/(?P<slug>[-\w]+)$',views.BlogDetail,name='detail'),
    # url(r'^search/',views.search,name='search'),
    # url(r'^blog/',views.blogFormView,name='blog'),
    # url(r'^reply/(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.ReplyPage,name='reply'),
    url('register',views.register,name='register'),
    url('logout', views.logoutUser, name="logout"),
    url('creategroup',views.create_group,name="create_group"),
    url('postcreate', views.create_post, name="postcreate"),
    url('comment', views.create_comment, name="comment"),
    url('reply', views.create_reply, name="reply"),
    url('joingroup', views.join_group, name="joingroup"),
    url('', views.loginUser, name="login"),
    url('home', views.home, name="home"),
    
    
    


####################################################################################################



    # url(r'^authorlist/',views.BlogAuthors,name='authorlist'),    
    # url(r'^author/(?P<id>\d+)$', views.BlogListByAuthor, name="blog-by-author"),
    # # url(r'^category/(?P<slug>[-\w]+)/$', views.base, name='category'),
    # # url(r'^cat/', views.base1, name='cat'),
    # # url(r'^subscribe/',views.sub,name='subscribe'),
    # # url(r'^contact/',views.Contact,name='contact'),


]
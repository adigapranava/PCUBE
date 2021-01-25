
from django.urls import path, include
from django.conf import settings
# from .views import PostListView, PostDetailView
from . import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import url



urlpatterns = [
    path('', views.filter, name='pcube-home'),
    path('allposts/', views.allposts, name='pcube-posts'),
    path('companynames/', views.send_company_name , name='pcube-company'),
    path('post/<int:pk>/', views.PostDetailView, name='post-detail'),
    path('post/<int:pk>/update/', views.UpdatePost, name='post-update'),
    path('likes/', views.like_post, name='post-like'),
    # path('buy/', views.buy_post, name='post-buy'),
    path('buy/', views.buy_post, name='post-buy'),
    path('search/', views.post_search_api, name='post-search'),
    path('sell/', views.sell_post, name='post-sell'),
    path('buyer_delete/', views.buyer_delete, name='post-buyer-delete'),
    path('addpost/', views.AddPost, name='add-post'),
    path('user/<str:username>/', views.UserPosts, name='user-posts'),
    path('notification/', views.notification, name='notification'),
    path('notification_delete/', views.notification_clear, name='noti-clear'),

    # quesitions
    path('askquesetion/', views.addques, name='ask-question'),
    path('ansquesetion/', views.addans, name='ans-question'),
    path('likequesetion/', views.likeques, name='like-question'),
]

import django.views.static
urlpatterns += [
   url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
   url(r'^media/(?P<path>.*)$', django.views.static.serve,{'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
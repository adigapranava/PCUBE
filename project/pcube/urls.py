
from django.urls import path
from django.urls import path, include
from django.conf import settings
# from .views import PostListView, PostDetailView
from . import views
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
    path('', views.filter, name='pcube-home'),
    path('allposts/', views.allposts, name='pcube-posts'),
    path('companynames/', views.send_company_name , name='pcube-company'),
    path('post/<int:pk>/', views.PostDetailView, name='post-detail'),
    path('post/<int:pk>/update/', views.UpdatePost, name='post-update'),
    path('likes/', views.like_post, name='post-like'),
    # path('buy/', views.buy_post, name='post-buy'),
    path('buy/', views.buy_post, name='post-buy'),
    path('addpost/', views.AddPost, name='add-post'),
    path('user/<str:username>/', views.UserPosts, name='user-posts'),
    path('about/', views.about, name='pcube-about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
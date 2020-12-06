
from django.urls import path
from django.urls import path, include
from django.conf import settings
from .views import PostListView, PostDetailView
from . import views
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
    path('', PostListView.as_view(), name='pcube-home'),
    path('allposts/', views.allposts, name='pcube-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.UpdatePost, name='post-update'),
    path('addpost/', views.AddPost, name='add-post'),
    path('about/', views.about, name='pcube-about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
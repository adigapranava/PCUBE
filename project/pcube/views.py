from django.shortcuts import render, redirect
from .models import Post
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

'''def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'pcube/home.html', context)'''

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name='pcube/home.html' #<app>/<model>_<view_type>.html
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

def AddPost(request):
    #login required
    if request.method == "POST":
        post = Post(title = request.POST['title'],
                    brand = request.POST['brand'],
                    discription = request.POST['product-disc'],
                    oldprice = int(request.POST['old-price']),
                    newprice = int(request.POST['new-price']),
                    owner = request.user,
                    address = request.user.profile.address,
                    phone = request.user.profile.phoneno,
                    state = request.user.profile.state,
                    city = request.user.profile.city,
                    image = request.FILES['img']
                    )
        post.save()
        messages.success(request, f"Posted Product Successfully")
        return HttpResponseRedirect("/post/{id}/".format(id= post.id))
    return render(request, 'pcube/addpost.html')


def UpdatePost(request, pk):
    #tODO: login required and owner == user?
    if request.method == "POST":
        post = Post.objects.get(id = pk)
        post.brand = request.POST['brand']
        post.title = request.POST['title']
        post.discription = request.POST['product-disc']
        post.oldprice = int(request.POST['old-price'])
        post.newprice = int(request.POST['new-price'])
        #tODO: changing the address and phone
        post.address = request.user.profile.address
        post.phone = request.user.profile.phoneno
        post.state = request.user.profile.state
        post.city = request.user.profile.city
        try:            
            post.image = request.FILES['img']
        except:
            pass        
        post.save()
        messages.success(request, f"Updated Product Successfully")
        return HttpResponseRedirect("/post/{id}/".format(id= post.id))
    post = Post.objects.get(id = pk)   
    context = {
        'post': post
    }
    return render(request, 'pcube/updatepost.html',context)

def about(request):
    return render(request, 'pcube/about.html')


# API OF ALL POSTS
def allposts(request):
    response = serializers.serialize('json', Post.objects.all())
    return HttpResponse(response, content_type='application/json')
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Post, Buy
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
import json
# Create your views here.

'''def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'pcube/home.html', context)'''


#add A post
def AddPost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            post = Post(title = request.POST['title'],
                        brand = request.POST['brand'],
                        discription = request.POST['product-disc'],
                        oldprice = int(request.POST['old-price']),
                        newprice = int(request.POST['new-price']),
                        post_type = request.POST['type'],
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
    else:
        request.session['prev'] = 'add-post'
        return redirect('login')

#detail view of a post and delete a post
def PostDetailView(request, pk):
    # if post exists?
    try:
        post = Post.objects.get(id = pk)
    except:
        return HttpResponseNotFound()
    
    # if method == POST delete the post
    if request.method == "POST":
        if(post.owner.username==str(request.user)):
            Post.objects.get(id = pk).delete()
            messages.success(request, f"Deleted the Post Successfully")
            return redirect('pcube-home')
        else:
          return HttpResponseNotFound("Forbidden")
    
    #check if user has liked the post
    is_liked = False
    is_requested = False
    buyers = Buy.objects.order_by('-price').filter(post_id = pk)

    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if Buy.objects.filter(post_id = pk, user_id = request.user.id).exists():
        is_requested = True

    context = {
        'object': post,
        'is_liked': is_liked,
        'is_requested': is_requested,
        'buyers': buyers,
        'total_likes': post.total_likes()
    }
    return render(request, 'pcube/post_detail.html',context)

# update a post
def UpdatePost(request, pk):
    # if user is logge in else go to login
    if request.user.is_authenticated:
        #if post exists
        try:
            post = Post.objects.get(id = pk)
        except:
            return HttpResponseNotFound()
        # if user is owner
        if(post.owner.username==str(request.user)):
            # print(type(request.user), post.owner.username)
            if request.method == "POST":
                post = Post.objects.get(id = pk)
                post.brand = request.POST['brand']
                post.title = request.POST['title']
                post.discription = request.POST['product-disc']
                post.oldprice = int(request.POST['old-price'])
                post.newprice = int(request.POST['new-price'])
                post.post_type = request.POST['type']
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
        else:
          return HttpResponseNotFound("Forbidden")            
    else:
        request.session['prev'] = f'/post/{pk}/update'
        return redirect('login')

# like a post
def like_post(request):
    # if logged in
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(id = request.POST.get('post_id'))
            is_liked = False
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                is_liked = False
            else:
                post.likes.add(request.user)
                is_liked = True
            return HttpResponseRedirect("/post/{id}/#like".format(id= post.id))
        except:
            return HttpResponseNotFound()
    else:
        request.session['prev'] = f"/post/{request.POST.get('post_id')}/#like"
        return redirect('login')

#buy post
def buy_post(request):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(id = request.POST.get('post_id'))
            if Buy.objects.filter(post_id = post, user_id = request.user).exists():
                Buy.objects.filter(post_id = post, user_id = request.user).delete()
            else:
                buyer = Buy(post_id = post, user_id = request.user, price = request.POST.get('price'))
                buyer.save()
            return HttpResponseRedirect("/post/{id}/#like".format(id= post.id))
        except:
            return HttpResponseNotFound()
    else:
        request.session['prev'] = f"/post/{request.POST.get('post_id')}/#like"
        return redirect('login')

#display all the post
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name='pcube/home.html' #<app>/<model>_<view_type>.html
    ordering = ['-date_posted']

# Render all the userames post
def UserPosts(request, username):
    try:
        user = User.objects.get(username = username)
        post = serializers.serialize('json', user.post_set.all())
        context = {
            'user': user,
            'post': post
        }
        return render(request, 'pcube/users_post.html',context)
    except:
        return HttpResponseNotFound()

def about(request):
    return render(request, 'pcube/about.html')


##Api handler
def filter(request):
    return render(request, 'pcube/filter.html')    

# API OF ALL POSTS
def allposts(request):
    response = serializers.serialize('json', Post.objects.all())
    return HttpResponse(response, content_type='application/json')

def send_company_name(request):
    f = open('/home/pranava_adiga/Desktop/PCUBE/project/pcube/company_name.json')
    response =  json.load(f)
    return JsonResponse(response)
    # return JsonResponse(response, safe = False)
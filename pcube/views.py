from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import (
    Post, Buy, Notification, 
    Question, Answer)
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.core import serializers
from django.db.models import Q
from django.http import (
    HttpResponse, HttpResponseRedirect, 
    JsonResponse, HttpResponseNotFound)
import json
import os
# Create your views here.

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'pcube/home.html', context)


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
    try:
        msg = Notification.objects.filter(post = post, user = request.user)        
    except:
        msg = []

    ques = Question.objects.filter(post = post)
    anss = Answer.objects.filter(post = post)

    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if Buy.objects.filter(post_id = pk, user_id = request.user.id).exists():
        is_requested = True

    context = {
        'object': post,
        'is_liked': is_liked,
        'is_requested': is_requested,
        'buyers': buyers,
        'total_likes': post.total_likes(),
        'msgs': msg,
        'questions': ques,
        'answers': anss
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
          return HttpResponseNotFound("<h1 style='color:blue'>Forbidden</h1>")
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
                price = Buy.objects.get(post_id = post, user_id = request.user).price
                Buy.objects.filter(post_id = post, user_id = request.user).delete()
                Notification.objects.filter(post = post, user=request.user).delete()
                Notification.objects.filter(post = post, user=post.owner).delete()
                ttl = "Your have canceled your Request"
                msg = "Your have cancelled your Request on "+ post.title + " for Rs " + str(price)
                noti = Notification(user = request.user, post = post, title =  ttl, discription=msg)
                noti.save()
            else:
                buyer = Buy(post_id = post, user_id = request.user, price = request.POST.get('price'))
                buyer.save()

                #msg to owner
                ttl = "Your have got an other coustomer"
                msg = "Your"+ post.title + " product is Requested for " + request.POST.get('price')+" by "+ request.user.username
                noti = Notification(user = post.owner, post = post, title =  ttl, discription=msg)
                noti.save()

                #msg to buyer
                ttl = "Your have requested a product"
                msg = "Your have Requested "+ post.title + " for Rs " + request.POST.get('price')
                noti = Notification(user = request.user, post = post, title =  ttl, discription=msg)
                noti.save()
            return HttpResponseRedirect("/post/{id}/#like".format(id= post.id))
        except:
            return HttpResponseNotFound()
    else:
        request.session['prev'] = f"/post/{request.POST.get('post_id')}/#like"
        return redirect('login')

def sell_post(request):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(id = request.POST.get('post_id'))
            user = User.objects.get(id = request.POST.get('user_id'))
            buyer = Buy.objects.get(post_id = post, user_id = user)

            post.sold = True
            post.soldto = user
            post.save()

            Notification.objects.filter(post = post, user=user).delete()
            Notification.objects.filter(post = post, user=post.owner).delete()

            #msg to other_buyer
            usrs_m = Notification.objects.filter(post = post)
            for usr_m in usrs_m:
                usr_m.title = "This product is sold out for Rs "+str(buyer.price)
                usr_m.dicsription = "Your request for "+post.title+" is rejected and was sold out"
                usr_m.save()

            #msg to owner
            ttl = "Your Product is sold"
            msg = "Your "+ post.title + " product is sold for Rs" + str(buyer.price) +" to "+ user.username + ".Their phone number "+ user.profile.phoneno
            noti = Notification(user = post.owner, post = post, title =  ttl, discription=msg)
            noti.save()

            #msg to selected_buyer
            ttl = "Your Request is approved"
            msg = "Your Request for "+ post.title + " for "+ str(buyer.price) + " is approved. You can contact Ph: "+ post.owner.profile.phoneno + " for more details."
            noti = Notification(user = user, post = post, title =  ttl, discription=msg)
            noti.save()

            Buy.objects.get(post_id = post).delete()
            return HttpResponseRedirect("/post/{id}/#buyer".format(id= post.id))
        except:
            return HttpResponseNotFound()
    else:
        request.session['prev'] = f"/post/{post.id}/#buyer"
        return redirect('login')

def buyer_delete(request):
    if request.user.is_authenticated:
        try:
            pst = Post.objects.get(id = request.POST.get('post_id'))
            usr = User.objects.get(id = request.POST.get('user_id'))
            if Buy.objects.filter(post_id = pst, user_id = usr).exists():
                price = Buy.objects.get(post_id = pst, user_id = usr).price
                Buy.objects.filter(post_id = pst, user_id = usr).delete()
                # Message to buyer:
                ttl = "Your Request was Rejected"
                msg = "Your request for "+pst.title+" product Rs"+ str(price) +" was rejected, Try once again!!"
                noti = Notification(user = usr, post = pst, title =  ttl, discription=msg)
                noti.save()
            return HttpResponseRedirect("/post/{id}/#buyer".format(id= pst.id))
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
        post = serializers.serialize('json', user.owner.all())
        context = {
            'user': user,
            'post': post
        }
        return render(request, 'pcube/users_post.html',context)
    except:
        return HttpResponseNotFound()

def notification(request):
    try:
        msgs = Notification.objects.order_by('-date_posted').filter(user = request.user, read = False)
        noti_count = msgs.count()
    except:
        msgs = []
        noti_count = 0
    context = {
        'msgs':msgs,
        'msgs_count': noti_count
    }
    return render(request, 'pcube/notification.html',context)

def notification_clear(request):
    noti = Notification.objects.get(id = request.POST['noti_id'])
    noti.read = True;
    noti.save();
    return redirect('notification')

def addques(request):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(id = request.POST.get('post_id'))
        except:
            return HttpResponseNotFound()
        ques = Question(post= post, user= request.user, ques= request.POST.get('question'))
        ques.save()
        # return redirect('post-detail', pk= request.POST.get('post_id'))
        return HttpResponseRedirect("/post/{id}/#ask".format(id= post.id))
    else:
        request.session['prev'] = f"/post/{request.POST.get('post_id')}/#ask"
        return redirect('login')

def addans(request):
    if request.user.is_authenticated:
        try:
            post = Post.objects.get(id = request.POST.get('post_id'))
        except:
            return HttpResponseNotFound()
        ques = Question(id= request.POST.get('ques-id'))
        # ques.is_answered = True
        # ques.save()
        ans = Answer(
            ques= ques,
            post= post, 
            ans=request.POST.get('answer')
            )
        ans.save()
        # return redirect('post-detail', pk= request.POST.get('post_id'))
        return HttpResponseRedirect("/post/{id}/#question-no-{qno}".format(
            id= post.id, 
            qno= ques.id)
            )
    else:
        request.session['prev'] = f"/post/{request.POST.get('post_id')}/#ask"
        return redirect('login')

##Api handler
def filter(request):
    return render(request, 'pcube/filter.html')    

# API OF ALL POSTS
def allposts(request):
    response = serializers.serialize('json', Post.objects.all())
    return HttpResponse(response, content_type='application/json')

def send_company_name(request):
    path =  os.path.abspath(os.getcwd())
    f = open(path+'/pcube/company_name.json')
    response =  json.load(f)
    return JsonResponse(response)
    # return JsonResponse(response, safe = False)

def post_search_view(request):
    return render(request, 'pcube/post_search.html')    

def post_search_api(request, *args, **kwargs):
    response = []
    if request.method == "GET":
        search_query = request.GET.get("q")
        search_results = []
        if len(search_query) > 0:
            search_results = Post.objects.filter(
                Q(title__icontains=search_query, sold = False)|
                Q(discription__icontains=search_query, sold = False)|
                Q(brand__icontains=search_query, sold = False)
                )

        response = serializers.serialize('json', search_results)

    return HttpResponse(response, content_type='application/json')
    
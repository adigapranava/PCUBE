from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Profile
from pcube.models import Post,Buy

# queue = []

# Create your views here.
def register(request):
    if request.method == "POST":
        if request.POST["password1"]==request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'users/register.html', {'error': "Username already exists"})
            except ObjectDoesNotExist:
                usr = User.objects.create_user(username= request.POST['username'],password= request.POST['password1'], email= request.POST['email'])
                #creating_a_profile_for_the_user
                pro = Profile(user = usr)
                pro.save()
                messages.success(request, f'Your account has been created! You are now able to log in')
                return redirect('login')
        else:
            return render(request, 'users/register.html', {'error': "Password Didn't Match"})
    else:   
        return render(request, 'users/register.html')


def login(request):
    if request.method == "POST":
        user = auth.authenticate(username=request.POST['username'], 
        password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            messages.success(request, f'Logged in successfully')
            #check if user details are filled?
            if(request.user.profile.phoneno  is None or
            request.user.profile.state is None or
            request.user.profile.city is None or
            request.user.profile.address is None):
                messages.success(request, f'Please fill your Details')
                return redirect('profile_update')
            try:   
                return redirect(request.session["prev"])
            except:
                return redirect('pcube-home')
        else:
            return render(request, 'users/login.html', {'error': "Invalid Login credientials."})
    else:
        return render(request, 'users/login.html')

def logout(request):
    auth.logout(request)
    return redirect('pcube-home')

def profile(request):
    try:
        user = User.objects.get(username=request.user)
        liked = Post.objects.filter(likes = user)
        bought = Post.objects.filter(soldto = user)
        sold = Post.objects.filter(owner = user, sold = True)
        unsold = Post.objects.filter(owner = user, sold = False)
        requested_b = Buy.objects.filter(user_id = user)
        requested = Post.objects.none()
        for re in requested_b:
            requested = requested | Post.objects.filter(id = re.post_id.id)
            
        

        context = {
            'liked': liked,
            'bought': bought,
            'sold': sold,
            'unsold': unsold,
            'requested': requested,
        }
        return render(request, 'users/profile.html',context)
    except:
        # queue.append('profile')
        request.session['prev'] = 'profile'
        return redirect('login')


def profile_update(request):
    try:
        user = User.objects.get(username=request.user)
    except:
        request.session['prev'] = 'profile_update'
        return redirect('login')
    if request.method == "POST":
        if(request.POST['address'] == "None" or 
        request.POST['phoneno'] == "None" or
        request.POST['state'] == "None" or 
        request.POST['city'] == "None"):
            messages.success(request, f'Please fill correct details')
            return redirect('profile_update')
        else:
            usr = request.user 
            pro = Profile.objects.get(user = usr)
            pro.fullname = request.POST['full-name'] 
            pro.address = request.POST['address']
            pro.phoneno = request.POST['phoneno']
            pro.city = request.POST['city']
            pro.state = request.POST['state']
            try:
                if request.FILES['pic']:
                    pro.image = request.FILES['pic']
            except:
                pass
            pro.save()
            messages.success(request, f"Updated Profile Successfully")
            return redirect('profile')
    
    else:
        return render(request, 'users/profile_update.html')

def aboutus(request):
    return render(request, 'users/ss.html')
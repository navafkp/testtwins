from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import cache_control, never_cache
from travelcompany.models import Places
from django.contrib.auth.models import User

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def userlogin(request):
    if 'adminname' in request.session and request.user.is_staff:
        return redirect('home')

    if request.user.is_authenticated:
        return redirect('mhome')
            
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if not(username):
            messages.info(request, "Please fill in all the required fields")
            return redirect('login')
        elif not(password):
            messages.info(request, "Please fill password")
            return redirect('login')
       
        user = None  
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.info(request, "Invalid Username")
            return redirect('login')
          
        if user is not None:
            data = authenticate(username=username, password=password)
            if data is not None:
                request.session['username'] = username
                login(request, data)
                return redirect('mhome')
                
            else:
                messages.info(request, "Invalid Password")
                return redirect('login')
              

    else:
        return render(request, 'login.html')


    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def register(request):
    if request.user.is_authenticated:
        return redirect('mhome')
    
    elif request.method == 'POST':
        first_name = request.POST.get('First_name')
        last_name = request.POST.get('Last_name')
        username = request.POST.get('Username')
        email = request.POST.get('Email')
        password1 = request.POST.get('Password1')
        password2 = request.POST.get('Password2')
        
        if not (first_name and last_name and username and email and password1 and password2):
            messages.info(request, "Please fill in all the required fields")
            return redirect('register')
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('register')
            
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email ID already taken")
                return redirect('register')
            
       
            else:
                user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                
                )
                user.set_password(password1)
                user.save()
            
                return redirect('login')
        else:
            messages.info(request, "Passowrd not matching")
            return redirect('register')
            
    return render(request, 'register.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def mhome(request):
    if 'adminname' in request.session:
        return redirect('home')
        
    elif 'username' in request.session:
        place = Places.objects.all()
        context = {
            'place' : place
        }
    
        return render(request, 'index.html', context)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache     
def Userlogout(request):
    if 'username' in request.session:
        del request.session['username']
        logout(request)
        return redirect('login')
    
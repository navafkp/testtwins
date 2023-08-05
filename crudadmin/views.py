from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import cache_control, never_cache
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @never_cache 
# def ADMINLOGIN(request):
#     if 'adminname' in request.session and request.user.is_staff:
#         return redirect('home')
#     if 'username' in request.session:
#         return redirect('mhome')
    
#     elif request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
#         if not(username):
#             messages.info(request, "Please fill in all the required fields")
#             return redirect('adminlogin')
#         elif not(password):
#             messages.info(request, "Please fill password")
#             return redirect('adminlogin')
        
        
#         user = None  
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             messages.info(request, "Invalid Username")
#             return redirect('adminlogin')
        
        
#         if user is not None:
#             if user.is_staff:
#                 data = authenticate(username=username, password=password)
#                 if data is not None:
#                     request.session['adminname'] = username
#                     login(request, data)
#                     return redirect('home')
                    
#                 else:
#                     messages.info(request, "Invalid Password")
#                     return redirect('adminlogin')
        
              

#     else:
#         return render(request, 'adminlogin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def ADMINLOGIN(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('home')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not (username and password):
            messages.error(request, "Please fill in all the required fields")
            return redirect('adminlogin')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "You are not authorized to access the admin page")
                
        else:
            
            messages.info(request, "Invalid username or password.")

    return render(request, 'adminlogin.html')  
       
print("hi") 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache 
def LOGOUT(request):
    if 'adminname' in request.session: 
        del request.session['adminname']
        logout(request)
        
    return redirect('adminlogin')
       


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache 
def home(request):
    if 'adminname' in request.session:
        users = User.objects.filter(is_staff=False).order_by('-id')
        paginator = Paginator(users, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        start_index = (page_obj.number - 1) * paginator.per_page + 1
        end_index = start_index + len(page_obj) - 1
        
        context = {
            'users': page_obj,
            'start_index': start_index,
            'end_index': end_index,
            'total_count': paginator.count,
        }
        return render(request, 'crudadmin.html', context)
        
    else:
        return redirect('adminlogin')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache 
def admin(request):
    if 'adminname' in request.session and request.user.is_staff:
        return redirect('home')
    
    if 'username' in request.session:
        return redirect('mhome')

    
    return render(request, 'adminlogin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache 
def ADD(request):
    if request.method == 'POST':
        first_name = request.POST.get('First_name')
        last_name = request.POST.get('Last_name')
        username = request.POST.get('Username')
        email = request.POST.get('Email')
        password1 = request.POST.get('Password1')
      
        
        if not (first_name and last_name and username and email and password1):
           messages.error(request, "Please fill in all the required fields.")
           return redirect('home')
   
            
           
        else:
           
            existing_user = User.objects.filter(username=username).first()
            if existing_user:
                messages.error(request, "Username already taken")
                return redirect('home')
            
            else:
               
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                )
                user.set_password(password1)
                user.save()
                
                messages.success(request, 'User created')
                return redirect('home')
    
    return render(request, 'crudadmin.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache 
def UPDATE(request, id):
    if request.method == 'POST':
        
        user = User.objects.get(id=id)

        user.first_name = request.POST.get('First_name')
        user.last_name = request.POST.get('Last_name')
        user.username = request.POST.get('Username')
        user.email = request.POST.get('Email')
        user.password = request.POST.get('Password')
        
        user.set_password(user.password)
        user.save()

        return redirect('home')
        
   

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache 
def DELETE(request, id):
    
    users = User.objects.filter(id=id)
    users.delete()
    
    context = {
        'users' : users,
    }
    return redirect('home')
   

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache 
def USEARCH(request):
    
    
    if request.method == 'POST':
        username = request.POST.get('name')
        username = username.strip()
        
        users = User.objects.filter(
            Q(username__istartswith=username) | Q(first_name__istartswith=username),
            is_staff=False
        )
        
        if not users.exists():
            messages.info(request, "There is no user with the name given")

     
        paginator = Paginator(users, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        start_index = (page_obj.number - 1) * paginator.per_page + 1
        end_index = start_index + len(page_obj) - 1
        
        
        context = {
            'users': page_obj,
            'start_index': start_index,
            'end_index': end_index,
            'total_count': paginator.count,
            
        }
        
        return render(request, 'search.html', context)
      
    return render(request, 'search.html')

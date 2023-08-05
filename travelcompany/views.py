from django.shortcuts import render,redirect
from .models import Places
from django.views.decorators.cache import cache_control, never_cache

# Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def mhome(request):
    if 'adminname' in request.session:
        return redirect('home')
        
    else:
        place = Places.objects.all()
        context = {
            'place' : place
        }
    
        return render(request, 'index.html', context)
    
    # return render(request, 'index.html')
    
    
    
    
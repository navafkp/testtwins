from django.urls import path

from . import views


urlpatterns = [
    path('', views.admin, name='adminlogin'),
    path('login/', views.ADMINLOGIN, name = 'clogin'),
    path('home/', views.home, name='home'), 
    path('add/', views.ADD, name='add'),  
    path('usearch/', views.USEARCH, name = 'usearch'),
    
    path('update/<int:id>/', views.UPDATE, name = 'update'),
    path('delete/<int:id>/', views.DELETE, name = 'delete'),
    path('logout/', views.LOGOUT, name = 'logout'),
   
 
]

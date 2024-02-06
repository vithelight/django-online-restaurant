from django.urls import path

from . import views

urlpatterns = [
    # Auth
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),
    
	path('', views.welcome, name='welcome'),
	path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
	path('cart/', views.cart, name='cart'),
	path('checkout/', views.checkout, name='checkout'),
	path('update_item/', views.updateItem, name='update_item'),
	path('process_order/', views.processOrder, name='process_order'),

]
import json
import datetime
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Auth
def loginPage(request):
     if request.user.is_authenticated:
          return redirect('home')
     else:
          if request.method == 'POST':
               username =  request.POST.get('username')
               password =  request.POST.get('password')
               user = authenticate(request, username=username, password=password)
               if user is not None:
                    login(request, user)
                    return redirect('home')
               else:
                    messages.info(request, 'Username or password is incorrect.')

          context = {}
          return render(request, 'rest/login.html', context)

def logoutPage(request):
     logout(request)
     return redirect('login')

@login_required(login_url='login')
def profile(request):
     context = {}
     return render(request, 'rest/profile.html', context)

def registerPage(request):
     if request.user.is_authenticated:
          return redirect('home')
     else:
          form = CreateUserForm()

          if request.method == 'POST':
               form = CreateUserForm(request.POST)
               if form.is_valid():
                    form.save()
                    messages.success(request, 'Account created successfully.')
                    return redirect('login')

          context = {'form': form}
          return render(request, 'rest/register.html', context)


def welcome(request):
     context = {}
     return render(request, 'rest/welcome.html',context)

@login_required(login_url='login')
def home(request):
     if request.user.is_authenticated:
          customer = request.user
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {
               'get_cart_total': 0,
               'get_cart_items': 0
          }
          cartItems = order['get_cart_items']
     context = {
          'products': Food.objects.all(),
          'cartItems': cartItems
     }
     return render(request, 'rest/home.html', context)

@login_required(login_url='login')
def cart(request):
     if request.user.is_authenticated:
          customer = request.user
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {
               'get_cart_total': 0,
               'get_cart_items': 0
          }
          cartItems = order['get_cart_items']
     context = {
          'items': items,
          'order': order,
          'cartItems':cartItems
     }
     return render(request, 'rest/cart.html', context)

@login_required(login_url='login')
def checkout(request):
     if request.user.is_authenticated:
          customer = request.user
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {
               'get_cart_total': 0,
               'get_cart_items': 0
          }
          cartItems = order['get_cart_items']
     context = {
          'items': items,
          'order': order,
          'cartItems':cartItems
     }
     return render(request, 'rest/checkout.html', context)

@login_required(login_url='login')
def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']
     print('productId: ', productId)
     print('action: ', action)

     customer = request.user
     product = Food.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, food=product)
     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)
     orderItem.save()
     if orderItem.quantity <= 0:
          orderItem.delete()
     return JsonResponse('Item was added.', safe=False)

@login_required(login_url='login')
def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          total = float(data['form']['total'])
          order.transaction_id = transaction_id
          if total == order.get_cart_total:
               order.complete = True
          order.save()
          ShippingAddress.objects.create(
               customer=customer,
               order=order,
               address=data['shipping']['address'],
               city=data['shipping']['city'],
               state=data['shipping']['state'],
               zipcode=data['shipping']['zipcode'],
               
          )
     else:
          print('User is not logged in')
     return JsonResponse('Payment complete', safe=False)
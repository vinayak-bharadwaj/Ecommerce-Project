from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, CartProduct
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime

# Create your views here.
class product_home (ListView):

    model = Product
    template_name = "products/product_home.html"
    context_object_name = "products"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = Order.objects.filter(user = self.request.user).get(placed = "False")
            cart = cart.items.all()
        else:
            cart = Order.objects.none()
        context['cart']=cart;
        return context

@login_required
def add_cart (request, pk):
    cart = Order.objects.filter(user = request.user).get(placed = "False")
    thing = Product.objects.get(id = pk)

    ThingInCart = cart.items.filter(product = thing)

    if ThingInCart.count() == 0:
        NewProd = CartProduct.objects.create(product = thing, quantity=request.POST.get('quantity'))
        cart.amount= cart.amount + (thing.price)*(int(request.POST.get('quantity')))
        cart.items.add(NewProd)
        cart.save()
    else:
        ThingInCart = cart.items.get(product = thing)
        cart.amount = cart.amount - (int(ThingInCart.quantity)) * (thing.price)
        ThingInCart.quantity=request.POST.get('quantity')
        cart.amount = cart.amount + (int(ThingInCart.quantity)) * (thing.price)
        ThingInCart.save()
        cart.save()
    messages.success(request, f'{thing.title} added to cart!')

    return redirect ('product-home')

@login_required
def remove_cart (request, pk):
    cart = Order.objects.filter(user = request.user).get(placed = "False")
    thing = Product.objects.get(id = pk)

    ThingInCart = cart.items.filter(product = thing)

    if ThingInCart.count() == 0:
        return HttpResponse("<h1>Product Not Ordered. Can't remove </h1>")
    else:
        ThingInCart = cart.items.get(product = thing)
        cart.amount = cart.amount - (thing.price)*(int(ThingInCart.quantity))
        cart.save()
        ThingInCart.delete()
        messages.success(request, f'{thing.title} removed from cart!')
            

    return redirect ('product-home')

class CartListView (ListView):
    model = CartProduct
    template_name = "products/cart.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        usr = get_object_or_404(User, username=self.request.user)
        qset = Order.objects.get(user = usr, placed = False).items.all()
        context = {"items":qset, "amount": Order.objects.get(user = usr, placed = False).amount}

        return context


class OrderListView (ListView):
    model = Order
    template_name = "products/orders.html"
    context_object_name = "orders"

    def queryset (self):
        usr = get_object_or_404(User, username=self.request.user)
        qset = Order.objects.filter(user = usr, placed = True).order_by('-order_time')

        return qset

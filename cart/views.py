from django.shortcuts import render
from products.models import Product 
from . models import Cart, CartItem
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def view_cart(request):
    try:
        user_cart = Cart.objects.get(user=request.user)
        cart_items = user_cart.cartitem_set.all()
        total_price = sum(item.sub_total() for item in cart_items)
    except Cart.DoesNotExist:
        user_cart = None
        cart_items = []
        total_price = 0

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'cart/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

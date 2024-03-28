from django.shortcuts import render, redirect 
import requests
import json
from cart.models import Cart
from .models import Order, OrderItem


def khalti_payment(request):
    user_cart = Cart.objects.get(user=request.user)
    cart_items = user_cart.cartitem_set.all()
    total_price = (sum(item.sub_total() for item in cart_items)) * 100
    total_display_price = sum(item.sub_total() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_display_price' : total_display_price
    }
    return render(request, 'order/payment.html', context)


def payment(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    return_url = request.POST.get('return_url')
    purchase_order_id = request.POST.get('purchase_order_id')
    amount = request.POST.get('amount')

    print("return_url",return_url)
    print("purchase_order_id",purchase_order_id)
    print("amount",amount)
    user = request.user

    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
        "name": user.username,
        "email": user.email,
        }
    })
    headers = {
        'Authorization': 'key bfc1a06e9a7741559698fdc766e01258',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    new_res = json.loads(response.text)
    print(new_res)
    return redirect(new_res['payment_url'])


def empty_cart_and_deduct_quantity(user):
    try:
        user_cart = Cart.objects.get(user=user)
        cart_items = user_cart.cartitem_set.all()
        
        for item in cart_items:
            product = item.product
            product.product_quantity -= item.quantity
            product.save()

        user_cart.cartitem_set.all().delete()

    except Cart.DoesNotExist:
        pass


def verify_payment(request):
    user = request.user
    user_cart = Cart.objects.get(user=user)
    cart_items = user_cart.cartitem_set.all()
    total_price = sum(item.sub_total() for item in cart_items) 
    shipping_address = user.address 

    order = Order.objects.create(user=user, total_price=total_price, shipping_address=shipping_address)

    for cart_item in cart_items:
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

    empty_cart_and_deduct_quantity(request.user)
    
    return render(request, 'order/verify_payment.html')


def order_history(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-order_date')
    context = {
        'user_orders': user_orders
    }
    return render(request, 'order/order_history.html', context)


def admin_view_orders(request):
    orders_with_details = Order.objects.select_related('user').prefetch_related('orderitem_set__product').all()

    context = {
        'orders_with_details': orders_with_details
    }
    return render(request, 'order/all_orders.html', context)
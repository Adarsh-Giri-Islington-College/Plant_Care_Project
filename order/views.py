from django.shortcuts import render, redirect 
import requests
import json
from cart.models import Cart
from .models import Order, OrderItem, Payment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def payment(request):
    payment_method_choices = Payment.PAYMENT_METHOD_CHOICES
    user_cart = Cart.objects.get(user=request.user)
    cart_items = user_cart.cartitem_set.all()
    total_price = (sum(item.sub_total() for item in cart_items)) * 100
    total_display_price = sum(item.sub_total() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_display_price' : total_display_price,
        'payment_method_choices': payment_method_choices
    }
    return render(request, 'order/payment.html', context)


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

    
def khalti_payment(request):
    payment_method = request.POST.get('payment_method')

    if payment_method == 'Khalti':
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
    else:
        return redirect('COD')


def verify_payment(request):
    payment_method = 'Khalti'
    payment_status = 'Done'

    payment = Payment.objects.create(payment_method=payment_method, payment_status=payment_status)

    user = request.user
    user_cart = Cart.objects.get(user=user)
    cart_items = user_cart.cartitem_set.all()
    total_price = sum(item.sub_total() for item in cart_items) 
    shipping_address = user.address 

    order = Order.objects.create(user=user, total_price=total_price, shipping_address=shipping_address, payment=payment)

    for cart_item in cart_items:
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

    empty_cart_and_deduct_quantity(request.user)
    
    return render(request, 'order/verify_payment.html')


def COD(request):
    payment_method = 'Cash on Delivery'
    payment_status = 'Pending'

    payment = Payment.objects.create(payment_method=payment_method, payment_status=payment_status)

    user = request.user
    user_cart = Cart.objects.get(user=user)
    cart_items = user_cart.cartitem_set.all()
    total_price = sum(item.sub_total() for item in cart_items) 
    shipping_address = user.address 

    order = Order.objects.create(user=user, total_price=total_price, shipping_address=shipping_address, payment=payment)

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
    orders_with_details = Order.objects.select_related('user').prefetch_related('orderitem_set__product').all().order_by('-order_date')
        
    paginator = Paginator(orders_with_details, 20)
    
    page_num = request.GET.get("page")
    try:
        orders = paginator.page(page_num)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    context = {
        'orders': orders,
    }
    return render(request, 'order/all_orders.html', context)
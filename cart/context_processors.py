from .models import Cart, CartItem

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                cart = Cart.objects.get(user=request.user)
            else:
                cart = Cart.objects.get(cart_id=request.session.session_key)
            
            cart_items = CartItem.objects.filter(cart=cart)
            
            cart_count = sum(item.quantity for item in cart_items)
        except Cart.DoesNotExist:
            cart_count = 0
            
    return {'cart_count': cart_count}

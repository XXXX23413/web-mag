from .cart import Cart

def cart(request):
    return {'cart_total_items': len (Cart(request))}
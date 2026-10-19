from decimal import Decimal
from .models import Product

class Cart:
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart 

    def add(self,product,quantity=1, update_quantity=False):
        if not product.is_active or product.stock_quantity <=0:
            return False
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price': str(product.price)}

        if update_quantity:
            new_quantity = quantity
        else:
            new_quantity = self.cart[product_id]['quantity'] + quantity

        if new_quantity > product.stock_quantity:
            new_quantity = product.stock_quantity

        if new_quantity <=0:
            del self.cart[product_id]
        else:
            self.cart[product_id]['quantity'] = new_quantity

        self.save()
        return True
    
    def remove(self,product):
        product_id  = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()         

    def save(self):
        self.session.modified =True

    def __iter__(self):
        product_ids = self.cart.keys()
        products =Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product']=product

        for item in cart.values():
            item['price']=Decimal(item['price'])
            item['total_price']=item['price']*item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.session.modified = True                        

                        

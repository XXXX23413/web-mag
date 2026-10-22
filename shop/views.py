from django.shortcuts import render, get_object_or_404
from .models import Product,Category,Brand
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from django.contrib import messages
from .forms import CartUpdateForm
from .forms import OrderForm
from .models import Order, OrderItem
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def catalog(request):
    products = Product.objects.filter(is_active=True).select_related('category','brand')
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)

    category_slug = request.GET.get('category')
    if category_slug:
        products=products.filter(category__slug=category_slug)

    brand_slug=request.GET.get('brand')
    if brand_slug:
        products=products.filter(brand__slug=brand_slug)

    search_query = request.GET.get('search')
    if search_query:
        products=products.filter(name__icontains=search_query)

    sort = request.GET.get('sort')
    if sort =='price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    context = {
        'products':products,
        'categories':categories,
        'brands':brands,
        'current_category':category_slug,
        'current_brand':brand_slug,
        'search_query':search_query,
        'current_sort':sort,
    }                        
    return render(request,'shop/catalog.html',context)
def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category','brand'),
        slug = slug,
        is_active=True
    )
    specifications = product.specification.all()

    context = {
        'product':product,
        'specifications':specifications,
    }
    return render(request, 'shop/product_detail.html',context)

@require_POST
def cart_add(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if cart.add(product=product,quantity=1):
        messages.success(request, f'<<{product.name}>> добавлен в корзину')
    else:
        messages.error(request, 'Товар недоступен или закончился на скаде')    
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart=Cart(request)
    return render(request,'shop/cart.html',{'cart':cart})

@require_POST
def cart_remove(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id = product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

@require_POST
def cart_update(request,product_id):
    cart=Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form =CartUpdateForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        if not cart.add(product=product,quantity=quantity,update_quantity=True):
            messages.error(request,'Товар недоступен')
        elif quantity > product.stock_quantity:
            messages.warning(request, f'На складе только {product.stock_quantity}шт.')

               
    else:
        messages.error(request,'Некорректное количество')

    return redirect('shop:cart_detail')    
@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart)==0:
        messages.warning(request,'Корзина пуста')
        return redirect('shop:cart_detail')

    if request.method == 'POST':
        form  = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user = request.user if request.user.is_authenticated else None,
                customer_name = form.cleaned_data['customer_name'],
                phone = form.cleaned_data['phone'],
                email = form.cleaned_data['email'],
                city = form.cleaned_data['city'],
                address = form.cleaned_data['address'],
                comment = form.cleaned_data['comment'],
                total_amount = cart.get_total_price(),
                number = f'ORD-{Order.objects.count() + 1:04d}',
            )

            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    product_name = item['product'].name,
                    quantity = item['quantity'],
                    price = item['price']
                )
            cart.clear()
            return redirect('shop:order_success', order_id=order.id)
    else:
        form = OrderForm()
    return render (request,'shop/checkout.html',{'cart':cart,'form':form})

def order_success(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,'shop/order_success.html',{'order':order}) 

def register_view(request):
    if request.user.is_authenticated:
        return redirect('shop:profile')

    if request.method =='POST':
        form =RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('shop:profile')
    else:
        form =RegisterForm()

    return render(request,'shop/register.html',{'form':form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:profile')

    if request.method =='POST':
        form = AuthenticationForm(request, data =request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'С возвращением, {user.username}!')
            next_url = request.GET.get('next', 'shop:profile')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request,'shop/login.html',{'form':form})

def logout_view(request):
    logout(request)
    messages.success(request,'Вы вышли из аккаунта')
    return redirect('shop:catalog')

@login_required
def profile (request):
    orders = Order.objects.filter(user = request.user).order_by('-created_at')
    return render(request, 'shop/profile.html',{'orders':orders})    

                               

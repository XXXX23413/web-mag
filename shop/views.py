from django.shortcuts import render, get_object_or_404
from .models import Product,Category,Brand
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from django.contrib import messages
from .forms import CartUpdateForm, OrderForm, SearchForm
from .models import Order, OrderItem
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.db import transaction
from django.core.paginator import Paginator

def catalog(request):
    form = SearchForm(request.GET)
    products = Product.objects.filter(is_active=True).select_related('category','brand')
    if form.is_valid():
        search_query = form.cleaned_data['search'].strip()
        category_slug=form.cleaned_data['category']
        brand_slug=form.cleaned_data['brand']
        sort =form.cleaned_data['sort']
    else:
        search_query = category_slug = brand_slug = sort = ''

    if category_slug:
        products=products.filter(category__slug = category_slug)
    if brand_slug:
        products =products.filter(brand__slug = brand_slug)
    if search_query:
        products = products.filter(name__icontains = search_query)

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort =='price_desc':
        products = products.order_by('-price')
    else:
        products=products.order_by('-created_at')

    categories = Category.objects.filter(is_active = True)
    brands = Brand.objects.filter(is_active=True)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'categories':categories,
        'brands':brands,
        'current_category':category_slug,
        'current_brand':brand_slug,
        'search_query':search_query,
        'current_sort':sort,
    }                       
    return render(request, 'shop/catalog.html', context)       

def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category','brand').prefetch_related('specification'),
        slug = slug,
        is_active = True
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
    try:
        quantity = int(request.POST.get('quantity',1))
    except (ValueError,TypeError):
        quantity=1

    if quantity < 1:
        quantity = 1
    if cart.add(product=product, quantity=quantity):
        messages.success(request, f'«{product.name}» ({quantity} шт.) добавлен в корзину')

    else:
        messages.error(request, 'Товар недоступен или закончился на складе')

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

def checkout(request):
    cart = Cart(request)

    if len(cart)==0:
        messages.warning(request,'Корзина пуста')
        return redirect('shop:cart_detail')

    if request.method == 'POST':
        form  = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    product_ids = [item['product'].id for item in cart]
                    locked ={
                        p.id: p for p in Product.objects.select_for_update().filter(id__in = product_ids)
                    }
                    for item in cart:
                        p = locked[item['product'].id]
                        if item['quantity'] > p.stock_quantity:
                            messages.error(
                                request,
                                f'Товар «{p.name}» закончился. Осталось {p.stock_quantity} шт.'
                            )
                            return redirect('shop:cart_detail')

                    order = Order.objects.create(
                        user = request.user if request.user.is_authenticated else None,
                        customer_name = form.cleaned_data['customer_name'],
                        phone = form.cleaned_data['phone'],
                        email = form.cleaned_data['email'],
                        city = form.cleaned_data['city'],
                        address = form.cleaned_data['address'],
                        comment = form.cleaned_data['comment'],
                        total_amount = cart.get_total_price(),
                )

                    for item in cart:
                        p = locked[item['product'].id]
                        OrderItem.objects.create(
                            order = order,
                            product = p,
                            product_name = p.name,
                            quantity = item['quantity'],
                            price = item['price']
                        )
                        p.stock_quantity -=item['quantity']
                        p.save(update_fields=['stock_quantity'])
                    cart.clear()
                    return redirect('shop:order_success', order_id=order.id)
            except Exception as e:
                messages.error(request,f'Ошибка:{e}')
                return redirect('shop:cart_detail')
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

@login_required
@require_POST
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id = order_id, user=request.user) 
    if order.status in ('new','processing'):
        for item in order.items.all():
            product = item.product
            product.stock_quantity += item.quantity
            product.save(update_fields = ['stock_quantity'])
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Заказ {order.number} отменён')
    else:
        messages.error(request, 'Этот заказ нельзя отменить')
    return redirect('shop:profile')            

def home(request):
    products = Product.objects.filter(is_active = True).select_related('category', 'brand').order_by('-created_at')[:6]
    return render(request,'shop/home.html',{'products': products})
                               

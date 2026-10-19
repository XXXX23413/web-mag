from django.shortcuts import render, get_object_or_404
from .models import Product,Category,Brand
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from django.contrib import messages
from .forms import CartUpdateForm

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

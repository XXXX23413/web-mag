from django.shortcuts import render
from .models import Product,Category,Brand

def catalog(request):
    products = Product.objects.filter(is_active=True)
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

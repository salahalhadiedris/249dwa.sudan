from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Category, Product

def category_list(request):
    """عرض جميع الفئات"""
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

def product_list(request, category_slug=None):
    """عرض المنتجات مع إمكانية الفلترة حسب الفئة"""
    categories = Category.objects.all()
    products = Product.objects.filter(in_stock=True)
    
    # فلترة حسب الفئة إذا كانت محددة
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        current_category = category
    else:
        current_category = None
    
    # الترقيم
    paginator = Paginator(products, 12)  # 12 منتج في الصفحة
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'products': page_obj,
        'current_category': current_category,
    }
    
    return render(request, 'products/product_list.html', context)

def filter_products_ajax(request):
    """فلترة المنتجات باستخدام AJAX"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        category_slug = request.POST.get('category_slug')
        
        products = Product.objects.filter(in_stock=True)
        
        if category_slug and category_slug != 'all':
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        
        # تحضير البيانات للرد
        products_data = []
        for product in products:
            products_data.append({
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'image_url': product.image.url if product.image else '',
                'url': product.get_absolute_url(),
                'category': product.category.name
            })
        
        return JsonResponse({
            'success': True,
            'products': products_data,
            'count': products.count()
        })
    
    return JsonResponse({'success': False, 'error': 'طلب غير صالح'})

def product_detail(request, product_slug):
    """تفاصيل المنتج"""
    product = get_object_or_404(Product, slug=product_slug)
    related_products = Product.objects.filter(
        category=product.category, 
        in_stock=True
    ).exclude(id=product.id)[:4]  # 4 منتجات ذات صلة
    
    context = {
        'product': product,
        'related_products': related_products
    }
    
    return render(request, 'products/product_detail.html', context)
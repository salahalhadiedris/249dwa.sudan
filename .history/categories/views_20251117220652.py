# views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

def product_list(request, category_slug=None):
    """عرض المنتجات مع إمكانية الفلترة حسب الفئة"""
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(in_stock=True)
    
    # فلترة حسب الفئة إذا كانت محددة
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        current_category = category
    else:
        current_category = None
    
    # الترقيم
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'products': page_obj,
        'current_category': current_category,
    }
    
    return render(request, 'pages/products.html', context)
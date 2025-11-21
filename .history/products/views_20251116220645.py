from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from .models import Product, Category, Pharmacy

def drugs_list_view(request):
    """
    عرض قائمة الأدوية مع إمكانية الفلترة حسب المدينة والفئة
    """
    # جلب جميع المنتجات
    products = Product.objects.filter(is_active=True)
    
    # فلترة حسب المدينة
    city = request.GET.get('city', '')
    if city:
        products = products.filter(city=city)
    
    # فلترة حسب الفئة
    category_id = request.GET.get('category', '')
    if category_id:
        try:
            products = products.filter(category_id=category_id)
        except ValueError:
            pass
    
    # جلب جميع الفئات للمنتجات
    categories = Category.objects.all()
    
    # جلب جميع المدن المتوفرة
    cities = Product.objects.values_list('city', flat=True).distinct().exclude(city__isnull=True).exclude(city='')
    
    context = {
        'products': products,
        'categories': categories,
        'cities': cities,
    }
    
    return render(request, 'product_list.html', context)


def get_pharmacies_for_product(request):
    """
    API endpoint لجلب الصيدليات المتوفرة لدواء معين
    """
    from django.http import JsonResponse
    
    product_id = request.GET.get('product_id')
    city = request.GET.get('city', '')
    
    if not product_id:
        return JsonResponse({'pharmacies': []})
    
    try:
        product = Product.objects.get(id=product_id)
        
        # جلب الصيدليات التي لديها هذا الدواء
        # يمكن أن يكون هناك علاقة many-to-many بين Product و Pharmacy
        # أو يمكن البحث عن الصيدليات في نفس المدينة
        pharmacies = Pharmacy.objects.filter(is_active=True)
        
        # إذا كان هناك فلتر مدينة، فلتر الصيدليات
        if city:
            pharmacies = pharmacies.filter(city=city)
        
        # إذا كان المنتج له علاقة مع الصيدليات
        if hasattr(product, 'pharmacies'):
            pharmacies = pharmacies.filter(id__in=product.pharmacies.all())
        
        pharmacies_data = []
        for pharmacy in pharmacies:
            pharmacies_data.append({
                'id': pharmacy.id,
                'name': pharmacy.name,
                'location': pharmacy.location or pharmacy.city,
                'city': pharmacy.city,
                'phone': pharmacy.phone or '',
                'whatsapp': pharmacy.whatsapp or pharmacy.phone or '',
                'image': pharmacy.image.url if pharmacy.image else None,
                'rating': getattr(pharmacy, 'rating', 4.5),
                'rating_count': getattr(pharmacy, 'rating_count', 0),
            })
        
        return JsonResponse({'pharmacies': pharmacies_data})
    
    except Product.DoesNotExist:
        return JsonResponse({'pharmacies': []})



def search_products(request):
    q = request.GET.get('q', '').strip()
    products = []

    if q:
        queryset = Product.objects.filter(name__icontains=q)[:10]
        for p in queryset:
            products.append({
                'id': p.id,
                'name': p.name,
                'name_english': p.name_english,
                'category': p.category.name if p.category else '',
                'image': p.image.url if p.image else '',
            })

    return JsonResponse({'products': products})


from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

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


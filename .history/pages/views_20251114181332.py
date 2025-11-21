from django.shortcuts import render,  get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from products.models import Product,Pharmacy,Category
# Create your views here.

def home(request):
    """
    عرض الصفحة الرئيسية - دليل الأدوية
    جميع البيانات تأتي من تطبيق المنتجات والفئات
    """
    # جلب جميع الفئات لعرضها في الصفحة
    categories = Category.objects.all().order_by('name')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'pages/home.html', context)


def products(request):
    """
    عرض قائمة الأدوية مع إمكانية الفلترة حسب المدينة والفئة والبحث
    """
    # جلب جميع المنتجات
    products = Product.objects.filter(is_active=True)
    
    # البحث بالاسم العربي أو الإنجليزي
    search = request.GET.get('search', '').strip()
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(name_english__icontains=search)
        )
    
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
    
    return render(request, 'pages/products.html', context)


def products(request):
    """
    API endpoint للبحث التلقائي عن المنتجات
    البحث بالاسم العربي أو الإنجليزي
    """
    from django.http import JsonResponse
    
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'products': []})
    
    # البحث في المنتجات النشطة بالاسم العربي أو الإنجليزي
    products = Product.objects.filter(
        is_active=True
    ).filter(
        Q(name__icontains=query) | 
        Q(name_english__icontains=query)
    )[:5]  # الحد الأقصى 5 نتائج للاقتراحات
    
    products_data = []
    for product in products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'name_english': product.name_english or '',
            'category': product.category.name if product.category else '',
            'price': str(product.price),
            'image': product.image.url if product.image else None,
        })
    
    return JsonResponse({'products': products_data})

def products(request):
        products = Product.objects.all()      
        return render(request, 'pages/products.html',{'products': products})


def pharmacies(request):
    """
    عرض قائمة الصيدليات مع إمكانية الفلترة حسب المدينة
    جميع البيانات تأتي من تطبيق الصيدليات فقط
    """
    # جلب جميع الصيدليات النشطة من تطبيق الصيدليات
    pharmacies = Pharmacy.objects.filter(is_active=True)
    
    # فلترة حسب المدينة (إذا تم اختيار مدينة)
    city = request.GET.get('city', '')
    if city:
        pharmacies = pharmacies.filter(city=city)
    
    # ترتيب الصيدليات حسب المميزة أولاً ثم التقييم ثم الاسم
    pharmacies = pharmacies.order_by('-is_featured', '-rating', 'name')
    
    # جلب جميع المدن المتوفرة من الصيدليات النشطة فقط
    # هذا يضمن أن أي صيدلية جديدة بمدينة جديدة ستظهر تلقائياً في الفلتر
    cities = Pharmacy.objects.filter(
        is_active=True
    ).values_list('city', flat=True).distinct().exclude(
        city__isnull=True
    ).exclude(
        city=''
    ).order_by('city')  # ترتيب المدن أبجدياً
    
    context = {
        'pharmacies': pharmacies,
        'cities': cities,
    }
    
    return render(request, 'pages/pharmacies.html', context)


def cosmo(request):
    return render(request, 'pages/cosmo.html')


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
    





def detalise(request):
    return render(request, 'pages/detalise.html')


def detalise(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # منتجات من نفس الفئة مع استبعاد المنتج نفسه
    similar_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:6]
    return render(request, 'products/detalise.html', {
        'product': product,
        'similar_products': similar_products,
    })




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
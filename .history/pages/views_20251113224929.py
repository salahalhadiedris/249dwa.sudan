from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from products.models import Product,Pharmacy,Category
# Create your views here.



def drug_directory_view(request):
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


def search_products_api(request):
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
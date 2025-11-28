from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product,Pharmacy
# Create your views here.


def home(request):
    return render(request, 'pages/home.html',)

def products(request):
        products = Product.objects.all()      
        return render(request, 'pages/products.html',{'products': products})


def pharmacies_list_view(request):
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
    
    return render(request, 'pharmacies.html', context)


def cosmo(request):
    return render(request, 'pages/cosmo.html')
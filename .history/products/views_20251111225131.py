from django.shortcuts import render
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
    
    return render(request, 'drugs-list.html', context)


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



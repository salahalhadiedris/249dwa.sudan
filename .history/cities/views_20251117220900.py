from django.shortcuts import render

# Create your views here.

def cities_list(request):
    return render(request, 'cities/city_list.html')
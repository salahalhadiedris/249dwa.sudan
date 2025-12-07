from django.shortcuts import render
from .models import Pharmacy

def pharmacies(request):
    pharmacies = Pharmacy.objects.all()
    return render(request, 'pharmacies/pharmacies.html', {'pharmacies': pharmacies})

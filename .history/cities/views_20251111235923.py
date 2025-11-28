from django.shortcuts import render

# Create your views here.
def Cities(request):
    return render(request, 'Cities_list.html')
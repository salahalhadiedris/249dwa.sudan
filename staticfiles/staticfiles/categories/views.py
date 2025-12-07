from django.shortcuts import render


def category_list_view(request):
    return render(request, 'categories/category_list.html')
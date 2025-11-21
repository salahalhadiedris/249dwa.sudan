from django.shortcuts import render

# Create your views here.
def user_profile_view(request):
    return render(request, 'users/user_profile.html')  
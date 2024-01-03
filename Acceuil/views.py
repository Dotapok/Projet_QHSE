from django.shortcuts import render

# Create your views here.
def acceuil(request):
    return render(request,'index.html')

def connexion(request):
    return render(request,'pages-login.html')

def inscription(request):
    return render(request,'register.html')

def mdpoublie(request):
    return render(request,'forgot-password.html')
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

def Dashboard(request):
    return render(request,'dashboard.html')

# fonctionalités
def connexionprocessus(request):
    return 

def inscriptionprocessus(request):
    return 

def mdpoublieprocessus(request):
    return 

# Pages standards
def AjouterAccident(request):
    return render(request,'Formulaire.html')

def tableauAction(request):
    return render(request,'tab_actions.html')

def profile(request):
    return render(request,'users-profile.html')
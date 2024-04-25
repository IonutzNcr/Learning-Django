from django.shortcuts import render, redirect
from django.views import View
from myapp.forms.login import UserForm
from myapp.forms.victory import VictoryForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User 
from .models import Victory
from django.utils import timezone
from cryptography.fernet import Fernet
from myapp.cript.key import key  
import re

cipher_suite = Fernet(key)


class HomeView(View):
    def get(self,request):
        context = {}
        return render(request,"home.html",context)
    
class LoginView(View):
    def get(self, request):
        form = UserForm()
        return render(request, "login.html", {'form':form})
    
    def post(self, request):
        user = authenticate(username = request.POST["username"], password = request.POST["password"])
        if user is not None:
            login(request, user)
            return redirect("victories")
        else: 
            form = UserForm()
            return render(request, "login.html", {'form':form})

class RegisterView(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form':form})
    def post(self, request):
        user = User.objects.create_user(request.POST["username"],request.POST["email"], request.POST["password"])
        user.save()
        return redirect("login")
        
    
    
class LogoutView(View):
    def get(self, request):
        #do something
        logout(request)
        return redirect("login")


class VictoryView(View):
    def get(self, request):
        if request.user.is_authenticated :
            victories = Victory.objects.all()
            if 'search' in request.GET:
                pattern = r"^@.+"
                is_search_by_username = re.match(pattern, request.GET['search'])
                if is_search_by_username:
                    username = re.sub("@","",request.GET['search'])
                    victories = victories.filter(user=username)
                else:
                    victories = victories.filter(content__icontains=request.GET['search'])
            return render(request, "victories.html", {'victories': victories})
        else :
            return redirect("login")
        

class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated :
            victories = Victory.objects.filter(user=request.user)
            search_str = ""
            if 'search' in request.GET:
                victories = victories.filter(content__icontains=request.GET['search'])
                search_str = "&search=" + request.GET['search']

            
            for victory in victories:
                url = "?d=" +  cipher_suite.encrypt(str(victory.id).encode()).decode()
                victory.url = url + search_str
            if 'd' in request.GET:
                # decrypt the value, send a signal to the template
                value = request.GET['d']
                victory_id = cipher_suite.decrypt(value).decode()
                for victory in victories:
                    if victory.id == int(victory_id):
                        victory.modify = True
                
            return render(request, "profile.html", {"victories":victories, "profile":request.user, })
        else :
            return redirect("login")
    
    def post(self, request):
        if 'update' in request.POST:
            victory = Victory.objects.get(id=int(request.POST["id"]))
            victory.content = request.POST["update"]
            victory.save()
            return redirect("/profile")
        form = VictoryForm()
        victories = Victory.objects.filter(user=request.user)
        if 'add' in request.POST:
            return render(request, "profile.html", {"victories":victories, "profile":request.user, "add": True, "form_add":form })
        elif 'content' in request.POST:
            victory = Victory(user = request.user.username, content = request.POST['content'], date = timezone.now())
            victory.save()
            return redirect("profile")
        else :
            return render(request, "profile.html", {"victories":victories, "profile":request.user})
        
"""
Controle the page that allows one to modify
their profile!
"""


class ProfileUpdateView (View):
    def get(self, request):
        user = request.user
        user = User.objects.get(username=user.username)
        return render(request,'profile-update.html',{'profile': user})
    
    def post(self, request):
        if 'id' in request.POST:
            user = User.objects.get(id=int(request.POST['id']))
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.save()
            return redirect('/profile')
        else:
            return redirect('/profile')
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ai_assistant.models import Conversation


def register_view(request):

    if request.method == 'POST':
        
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        


        if not name or not email or not username or not password or not confirm_password:
            messages.error(request, "All fields are required")
            return render(request, 'register.html')
        
        
        elif User.objects.filter(email = email).exists():
            messages.error(request,"Email Already exists")
            return render(request, 'register.html')
        
        
        elif User.objects.filter(username = username).exists():
            messages.error(request,"Username already exists")
            return render(request, 'register.html')
        
        
        elif password != confirm_password:
            messages.error(request, "Password does not matching")
            return render(request, 'register.html')
        
        
        elif len(password) < 8:
            messages.error(request, "Password must be at least 6 characters")
            return render(request, 'register.html')
        
        
        user = User(first_name = name, email = email, username = username)
        user.set_password(password)
        user.save()

        login(request, user)
        
        return redirect('all-books')

    return render(request, 'register.html')


def signin_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        
        if user:
            login(request, user)
            
            next_url = request.POST.get('next')

            if next_url:
                return redirect(next_url)
            
            return redirect('all-books')
        
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "signin.html")

def logout_view(request):

    if request.user.is_authenticated:
        Conversation.objects.filter(user = request.user).delete()

    logout(request)
    return redirect('all-books')
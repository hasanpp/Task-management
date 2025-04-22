from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not (username or password) :
            messages.error(request, "Username and Password are required.")
            return redirect('login')
            
        elif len(username.replace(" ","")) == 0 or len(password.replace(" ","")) == 0:
            messages.error(request, "Username and Password can't be empty.")
            return redirect('login')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if hasattr(user, 'role') and (user.role == 'admin' or user.role == 'superadmin'):
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "You don't have permission to access admin panel.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    
    return render(request, 'auth/login.html')

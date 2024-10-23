from django.shortcuts import render, redirect
from shop.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('product_list')
        else:
            messages.error(request,
                            'Invalid username or password.')
            pass
    else:
      form = LoginForm()
      return render(request,'shop/auth/login.html', {form:form})

def register_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = authenticate(request, username=username, password=password, email=email)
            if user:
                login(request, user)
                return redirect('product_list')
        else:
            messages.error(request,
                            'Invalid username or password.')
            pass
    else:
      form = LoginForm()
    return render(request,'shop/auth/register.html', {form:form})


def logout_page(request):
    if request.method == 'POST':
     logout(request)
    return redirect('product_list')

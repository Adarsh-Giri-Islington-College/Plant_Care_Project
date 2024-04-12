from django.shortcuts import render, redirect, get_object_or_404
from .models import User, edit_profile_form
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.core.mail import send_mail


def is_admin(user):
    return user.is_authenticated and (user.user_role == User.ADMIN or user.user_role == User.STAFF)


def is_not_banned(user):
    return not user.is_banned


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        user_image = request.FILES.get('user_image')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                print('Username exists! Please try another username')
                username_error_message = 'Username exists! Please try another username'
                context = {
                    'username_error_message': username_error_message
                }
                return render(request, 'users/register.html', context)
            elif User.objects.filter(email=email).exists():
                print('Email exists! Please try another email')
                email_error_message = 'Email exists! Please try another email'
                context = {
                    'email_error_message': email_error_message
                }                
                return render(request, 'users/register.html', context)
            else:
                user = User.objects.create_user(user_image=user_image, username=username, email=email, first_name=first_name, last_name=last_name, address=address, password=password1)
                user.save()
                return redirect('login')
        else:
            error_message = 'Passwords did not match!'
            context = {
                'error_message': error_message
            }
            return render(request, 'users/register.html', context)
    else:
        return render(request, 'users/register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None and is_not_banned(user):
            if user.user_role == 'user':
                auth.login(request, user)
                print('Login Successful!')
                return redirect('display_products')
            else:
                auth.login(request, user)
                request.session.set_expiry(0)  
                return redirect('admin_dashboard')
        elif user is not None and user.is_banned:
            ban_until = user.ban_until.strftime("%Y-%m-%d %H:%M:%S") if user.ban_until else None
            error_message = 'Sorry you have been banned until ' + ban_until + '.'
            context = {
                'error_message': error_message
            } 
            return render(request, 'users/login.html', context)
        else:
            error_message = 'User not Found!'
            context = {
                'error_message': error_message
            }            
            return render(request, 'users/login.html', context)
    else:
        return render(request, 'users/login.html') 


def admin_dashboard(request):
    user = request.user  
    context = {'user': user}
    return render(request, 'users/admin_dashboard.html', context)


@login_required
def logout(request):
    auth.logout(request)
    print('User is logged out')
    return redirect('display_products')


@login_required
def view_profile(request):
    user = request.user  
    context = {'user': user}
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = edit_profile_form(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = edit_profile_form(instance=user)

    context = {'form': form}
    return render(request, 'users/edit_profile.html', context)


@user_passes_test(is_admin)
def view_users(request):
    users = User.objects.all()
    user_role_choices = User.ROLE_CHOICES 
    context = {'users': users, 'user_role_choices': user_role_choices}
    return render(request, 'users/view_users.html', context)


@user_passes_test(is_admin)
def edit_user_details(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        user_role = request.POST.get('user_role') 
        if user_role in dict(User.ROLE_CHOICES):
            user.user_role = user_role
            user.save()
            return redirect('view_users')

    context = {'user': user}
    return render(request, 'users/view_users.html', context)


@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('view_users')


@user_passes_test(is_admin)
def ban_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        try:
            ban_duration_days = int(request.POST.get('ban_duration_days'))
        except ValueError:
            return render(request, 'users/view_users.html', {'user': user, 'error_message': "Invalid ban duration"})
        
        user.is_banned = True
        user.ban_until = timezone.now() + timezone.timedelta(days=ban_duration_days)
        user.save()
        return redirect('view_users')
    
    context = {'user': user}
    return render(request, 'users/view_users.html', context)


@user_passes_test(is_admin)
def unban_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        user.is_banned = False
        user.ban_until = None
        user.save()
        return redirect('view_users')
    
    context = {'user': user}
    return render(request, 'users/view_user.html', context)
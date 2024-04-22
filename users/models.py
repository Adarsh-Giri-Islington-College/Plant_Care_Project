from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, user_image, username, email, first_name, last_name, address, is_banned=False, ban_until=None, created_time=None, password=None, is_staff=False, is_active = False):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        
        if not user_image:
            user_image = 'user_images/profile_image.jpg'
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            address=address,
            user_image=user_image,
            is_banned=is_banned,
            ban_until=ban_until,
            created_time=created_time,
            is_staff=is_staff,
            is_active=is_active,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, first_name, last_name, address, password, user_image=None, created_time=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            address=address,
            user_image=user_image,
            is_staff=True,  
            created_time=created_time,
        )
        user.user_role = User.ADMIN 
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    ADMIN = 'admin'
    USER = 'user'
    STAFF = 'staff'

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (USER, 'user'),
        (STAFF, 'staff'),
    )
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True, null=False, blank=False)
    username = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    address = models.CharField(max_length=50)
    user_role = models.CharField(max_length=5, choices=ROLE_CHOICES, default=USER)
    user_image = models.ImageField(upload_to='images/user_images/', null=True, blank=True, default='images/user_images/profile_image.jpg') 
    is_banned = models.BooleanField(default=False)
    ban_until = models.DateTimeField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'address']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True


class edit_profile_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_image', 'email', 'username', 'first_name', 'last_name', 'address']
        widgets = {
            'user_image' : forms.FileInput({'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


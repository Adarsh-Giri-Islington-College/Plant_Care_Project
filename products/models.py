from django.db import models
from datetime import datetime
from django import forms
import json
from users.models import User

class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    product_image = models.ImageField(null=False, blank=False)
    product_name = models.CharField(max_length=200, null=False, blank=False)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = models.IntegerField(null=False, blank=False)
    product_description = models.TextField()  
    product_for = models.CharField(max_length=500, null=True, blank=True)  
    added_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.product_name


class product_form(forms.ModelForm):
    product_for_choices = [(value[0], value[0]) for value in json.load(open('./models/class_names.json')).values() if isinstance(value, list) and len(value) > 0]
    product_for = forms.MultipleChoiceField(choices=product_for_choices, required=False, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Product
        fields = ('product_image', 'product_name', 'product_price', 'product_quantity', 'product_description', 'product_for')
        widgets = {
            'product_image': forms.FileInput(attrs={'class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_price': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'product_quantity': forms.TextInput(attrs={'class': 'form-control'}),
            'product_description': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean_product_for(self):
            product_for_data = self.cleaned_data['product_for']
            if not product_for_data:
                return None
            return product_for_data


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    rating_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f"Cart {self.rating_id}"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
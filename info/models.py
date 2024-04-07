from django.db import models
from django import forms
import json


class Plant_Info(models.Model):
    plant_id = models.BigAutoField(primary_key=True)
    plant_image = models.ImageField(null=False, blank=False)
    plant_common_name = models.CharField(max_length=50)
    plant_scientific_name = models.CharField(max_length=50)
    is_affected = models.BooleanField(default=False)
    disease_name = models.CharField(max_length=50)
    plant_description = models.TextField()  
    cause = models.CharField(max_length=50)
    solution = models.CharField(max_length=50)

    def __str__(self):
        return self.plant_common_name
    

class Plant_Form(forms.ModelForm):
       
    class Meta:
        model = Plant_Info
        fields = ('plant_image', 'plant_common_name', 'plant_scientific_name', 'is_affected', 'disease_name', 'plant_description', 'cause', 'solution')
        widgets = {
            'plant_image': forms.FileInput(attrs={'class': 'form-control'}),
            'plant_common_name': forms.TextInput(attrs={'class': 'form-control'}),
            'plant_scientific_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_affected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'disease_name': forms.TextInput(attrs={'class': 'form-control'}),
            'plant_description': forms.Textarea(attrs={'class': 'form-control'}),
            'cause': forms.TextInput(attrs={'class': 'form-control'}),
            'solution': forms.TextInput(attrs={'class': 'form-control'}),
        }
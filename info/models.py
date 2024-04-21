from django.db import models
from django import forms
import json


class Plant_Info(models.Model):
    plant_id = models.BigAutoField(primary_key=True)
    plant_image = models.ImageField(null=False, blank=False)
    plant_name = models.CharField(max_length=50)
    is_affected = models.BooleanField(default=False)
    plant_description = models.TextField()  
    cause = models.TextField(max_length=50)
    solution = models.TextField(max_length=50)

    def __str__(self):
        return self.plant_name
    

class Plant_Form(forms.ModelForm):
    plant_for_choices = [(value[0], value[0]) for value in json.load(open('./models/class_names.json')).values() if isinstance(value, list) and len(value) > 0]
    plant_name = forms.ChoiceField(choices=plant_for_choices, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Plant_Info
        fields = ('plant_image', 'plant_name', 'is_affected', 'plant_description', 'cause', 'solution')
        widgets = {
            'plant_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_affected': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'plant_description': forms.Textarea(attrs={'class': 'form-control'}),
            'cause': forms.Textarea(attrs={'class': 'form-control'}),
            'solution': forms.Textarea(attrs={'class': 'form-control'}),
        }
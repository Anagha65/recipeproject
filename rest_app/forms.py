from django import forms
from .models import *

class RecipesForm(forms.ModelForm):
    class Meta:
        model = Recipes
        fields = '__all__'
from django import forms
from .models import Meal

class MealLogForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'calories', 'protein', 'carbs', 'fat']

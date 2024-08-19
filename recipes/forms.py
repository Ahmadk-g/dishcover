from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Recipe, CATEGORIES


class RecipeForm(forms.ModelForm):
    """ Form to create recipe """
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image', 'image_alt', 'category', 'calories']
        
        widgets = {
            'ingredients': SummernoteWidget(),
            'instructions': SummernoteWidget(),
        }
        
        labels = {
            'title': 'Recipe Title',
            'description': 'Description',
            'ingredients': 'Recipe Ingredients',
            'instructions': 'Recipe Instructions',
            'image': 'Recipe Image',
            'image_alt': 'Describe Image',
            'category': 'Meal Category',
        }
       
       
class CategoryFilterForm(forms.Form):
    
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + list(CATEGORIES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),  # Bootstrap class for styling
        label='Meal Type'
    )
    
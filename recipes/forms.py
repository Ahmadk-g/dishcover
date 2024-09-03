from django import forms
from django_summernote.widgets import SummernoteWidget # Import SummernoteWidget to use rich text editor for form fields
from .models import Recipe, CATEGORIES


class RecipeForm(forms.ModelForm):
    """ Form to create recipe """
    class Meta:
        # Specifies the model to be used for this form
        model = Recipe 
        # Fields from the Recipe model that will be included in the form
        fields = ['title', 'description', 'ingredients', 'instructions', 'image', 'image_alt', 'category', 'calories']
        
        # Specifies custom widgets for form fields
        widgets = {
            'ingredients': SummernoteWidget(), # Use Summernote rich text editor
            'instructions': SummernoteWidget(),
        }
        
        # Customizes the labels for each form field to be displayed in the form
        labels = {
            'title': 'Recipe Title',
            'description': 'Description',
            'ingredients': 'Recipe Ingredients',
            'instructions': 'Recipe Instructions',
            'image': 'Recipe Image',
            'image_alt': 'Describe Image',
            'category': 'Meal Category',
        }
       

# This form is not tied to a model; it's a simple form with a single ChoiceField for filtering recipes by category
class CategoryFilterForm(forms.Form):
    """ 
    Form for filtering recipes by category. 
    This form allows users to select a meal category to filter the displayed recipes.
    """
    category = forms.ChoiceField(
        
        # Adds a default "All Categories" option to the category choices
        choices=[('', 'All Categories')] + list(CATEGORIES),
        
        required=False, # The category field is optional
        widget=forms.Select(attrs={'class': 'form-select'}), # Uses Bootstrap's form-select class for styling
        label='Meal Type'  # Custom label for the category field
    )
    
from django import forms
from .models import CollaborateRequest


class CollaborateForm(forms.ModelForm):
    """ 
    Form class for users to request a collaboration. 
    """
    class Meta:
        """ 
        Based on the CollaborateRequest model and order of the fields
        """
        model = CollaborateRequest
        fields = ('name', 'email', 'message')
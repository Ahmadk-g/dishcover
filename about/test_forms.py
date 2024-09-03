from django.test import TestCase
from .forms import CollaborateForm


class TestCollaborateForm(TestCase):
    """ 
    Test cases for the CollaborationForm to ensure it validates input correctly 
    """

    def test_form_is_valid(self):
        """ Test that the form is valid with all required fields provided."""
        
        # Create an instance of the form with valid data
        form = CollaborateForm({
            'name': 'Ahmad',
            'email': 'test@test.com',
            'message': 'Hello!'
        })
        # Assert that the form is valid
        self.assertTrue(form.is_valid(), msg="Form is not valid")
    
    def test_name_is_required(self):
        """ Test that the form is invalid when name field is missing"""
        
        # Create an instance of the form with an empty name field
        form = CollaborateForm({
            'name': '',
            'email': 'test@test.com',
            'message': 'Hello!'
        })
        # Assert that the form is invalid
        self.assertFalse(form.is_valid(), msg="Name was not provided, but the form is valid")
        
    def test_email_is_required(self):
        """Test that the form is invalid when the email field is missing."""
        
        form = CollaborateForm({
            'name': 'Ahmad',
            'email': '',
            'message': 'Hello!'
        })
        self.assertFalse(form.is_valid(), msg="Email was not provided, but the form is valid")
        
    def test_message_is_required(self):
        """  Test that the form is invalid when the message field is missing. """
        form = CollaborateForm({
            'name': 'Ahmad',
            'email': 'test@test.com',
            'message': ''
        })
        self.assertFalse(form.is_valid(), msg="Message was not provided, but the form is valid")
        
    def test_form_is_empty(self):
        """ Test that the form is invalid when no data is provided """
        # Create an instance with no data
        form = CollaborateForm(data={})
        # Assert that the form is invalid and has the correct number of errors
        self.assertFalse(form.is_valid(),)
        self.assertEqual(len(form.errors), 3) # Expecting 3 fields to be missing
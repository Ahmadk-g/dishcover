from django.test import TestCase
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO  # to handle byte data in memory
from .models import User
from .forms import RecipeForm, CategoryFilterForm
import os


class RecipeFormTests(TestCase):
    """Test suite for validating RecipeForm and CategoryFilterForm."""

    def setUp(self):
        """Set up a test user and sample image for form tests"""
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Load a static image file for testing
        static_image_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'static', 'images', 'nobody.jpg'
        )
        with open(static_image_path, 'rb') as img:
            image_content = img.read()

        # Create an InMemoryUploadedFile instance to simulate an uploaded image
        self.image = InMemoryUploadedFile(
            file=BytesIO(image_content),  # To simulate a file-like object
            field_name='image',
            name='nobody.jpg',
            content_type='image/jpeg',
            size=len(image_content),
            charset=None
        )

    def test_recipe_form_valid(self):
        """Test RecipeForm with valid data"""

        # Define form data with valid values
        form_data = {
            'title': 'Valid Recipe',
            'description': 'A valid description',
            'ingredients': 'Valid ingredients',
            'instructions': 'Valid instructions',
            'image': self.image,
            'image_alt': 'A valid image',
            'category': 'main dishes',
            'calories': 150
        }

        # Create a form instance with the provided data and image file
        form = RecipeForm(data=form_data, files={'image': self.image})
        # Assert that the form is valid
        self.assertTrue(form.is_valid())

    def test_recipe_form_invalid(self):
        """Test RecipeForm with missing required fields"""

        # Define form data with a missing title (required field)
        form_data = {
            'title': '',  # Title is required
            'description': 'Description without title',
            'ingredients': 'Valid ingredients',
            'instructions': 'Valid instuctions',
            'image': self.image,
            'image_alt': 'A valid image',
            'category': 'main dishes',
            'calories': 150
        }
        form = RecipeForm(data=form_data, files={'image': self.image})
        self.assertFalse(form.is_valid())

        # Assert that there is exactly one error (the missing title)
        self.assertEqual(len(form.errors), 1)

    def test_category_filter_form_valid(self):
        """Test CategoryFilterForm with valid data"""

        form_data = {
            'category': 'appetisers/snacks'
        }

        form = CategoryFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_filter_form_invalid(self):
        """Test CategoryFilterForm with invalid data"""

        form_data = {
            'category': 'invalid_category'  # This should not be in the choices
        }

        form = CategoryFilterForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Assert that 'category' is present in form errors
        self.assertIn('category', form.errors)

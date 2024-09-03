from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile # allows us to create a mock image file that can be used for testing
from django.contrib.auth import get_user_model
from .models import Recipe
from io import BytesIO # used here to simulate file-like behavior with byte data, allowing us to create a file-like object from a byte string.
import os

# Get user model
User = get_user_model()

class RecipeTests(TestCase):
    
    def setUp(self):
        """
        Set up a test user and a sample recipe for testing.
        - Creates a user and logs in.
        - Loads a sample image for testing.
        - Create a Recipe instance for testing.
        """
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Load a static image file for testing from the root directory for testing
        image_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'nobody.jpg'
        )
        with open(image_path, 'rb') as img:
            image_content = img.read()

        # Create an InmemoryUploadedFile onject
        self.image = InMemoryUploadedFile(
            file=BytesIO(image_content), # Use BytesIO to simulate a file-like object
            field_name='image',
            name='nobody.jpg',
            content_type='image/jpeg',
            size=len(image_content),
            charset=None
        )
        # Create a sample Recipe instance
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            slug='test-recipe',
            author=self.user,
            description='Test description',
            ingredients='Test ingredients',
            instructions='Test instructions',
            image=self.image,
            image_alt='Test image',
            category='appetisers/snacks',
            calories=200
        )
        
    def test_recipe_list_view(self):
        """
        Test that the recipes list view renders correctly.
        - Sends a GET request to the recipes list view.
        - Checks that the response status is 200 OK.
        - Ensures the correct template is used and the recipe title is present in the response.
        """

        response = self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes.html')
        self.assertContains(response, self.recipe.title)

    

    def test_recipe_details_view(self):
        """
        Test that the recipe detail view renders correctly.
        - Sends a GET request to the recipe details view for the created recipe.
        - Checks that the response status is 200 OK.
        - Ensures the correct template is used and the recipe details are present in the response.
        """

        response = self.client.get(reverse('recipe_details', kwargs={'slug': self.recipe.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_details.html')
        self.assertContains(response, self.recipe.title)
        self.assertContains(response, self.recipe.ingredients)

    

    def test_add_recipe_view_valid(self):
        """
        Test adding a recipe with valid data.
        - Sends a POST request to add a new recipe with valid form data.
        - Checks that the response status is 200 (redirect after successful form submission).
        - Ensures that the new recipe is not saved (indicating the form didn't save the recipe).
        """
        form_data = {
            'title': 'New Recipe',
            'description': 'New description',
            'ingredients': 'New ingredients',
            'instructions': 'New instructions',
            'image': self.image,
            'image_alt': 'New image',
            'category': 'desserts',
            'calories': 150
        }
        response = self.client.post(reverse('add_recipes'), data=form_data)
        self.assertEqual(response.status_code, 200)  # Redirect after successful form submission
        self.assertFalse(Recipe.objects.filter(title='New Recipe').exists())
        

    def test_edit_recipe_view_valid(self):
        """
        Test updating a recipe with valid data.
        - Sends a POST request to update the existing recipe with new data.
        - Checks that the response status is 200 (redirect after successful update).
        - Ensures that the recipe has been updated with the new data.
        """
        
        form_data = {
            'title': 'Updated Recipe',
            'description': 'Updated description',
            'ingredients': 'Updated ingredients',
            'instructions': 'Updated instructions',
            'image': self.image,
            'image_alt': 'Updated image',
            'category': 'salads',
            'calories': 250
        }
        response = self.client.post(reverse('edit_recipe', kwargs={'slug': self.recipe.slug}), data=form_data)
        self.assertEqual(response.status_code, 200)  # Redirect after successful post
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Test Recipe')
        

    def test_delete_recipe_view(self):
        """
        Test deleting a recipe.
        - Sends a POST request to delete the existing recipe.
        - Checks that the response status is 302 (redirect after successful deletion).
        - Ensures that the recipe no longer exists in the database.
        """
        
        response = self.client.post(reverse('delete_recipe', kwargs={'slug': self.recipe.slug}))
        self.assertEqual(response.status_code, 302) # Redirect after successful deletion
        self.assertFalse(Recipe.objects.filter(title='Test Recipe').exists())
        

    def test_like_recipe_view(self):
        """
        Test liking and unliking a recipe.
        - Sends a GET request to like the recipe.
        - Checks that the response status is 302 (redirect after liking).
        - Verifies that the recipe is now liked by the user.
        - Sends another GET request to unlike the recipe.
        - Checks that the recipe is no longer liked by the user.
        """
        response = self.client.get(reverse('like_recipe', kwargs={'slug': self.recipe.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.recipe.likes.filter(id=self.user.id).exists())

        # Unliking the recipe
        response = self.client.get(reverse('like_recipe', kwargs={'slug': self.recipe.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.recipe.likes.filter(id=self.user.id).exists())
        
      

    def test_favorites_view(self):
        """
        Test that the favorites view displays the user's liked recipes.
        - Adds the recipe to the user's liked recipes.
        - Sends a GET request to the favorites view.
        - Checks that the response status is 200 OK.
        - Ensures that the correct template is used and the recipe title is displayed.
        """

        self.recipe.likes.add(self.user)
        
        response = self.client.get(reverse('favorites'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/favorites.html')
        self.assertContains(response, self.recipe.title)

    

    def test_my_recipes_view(self):
        """
        Test that the my recipes view displays the recipes authored by the user.
        - Sends a GET request to the my recipes view.
        - Checks that the response status is 200 OK.
        - Ensures that the correct template is used and the recipe title is displayed.
        """
        
        response = self.client.get(reverse('my_recipes'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/myrecipes.html')
        self.assertContains(response, self.recipe.title)

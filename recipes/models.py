from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField



# Create your models here.

# Choice Fields
CATEGORIES = (
    ('appetisers', 'Appetizers'),
    ('beverages', 'Beverages'),
    ('soups', 'Soups'),
    ('salads', 'Salads'),
    ('vegan', 'Vegan'),
    ('vegeterian', 'Vegeterian'),
    ('main dishes', 'Main Dishes'),
    ('desserts', 'Desserts')
)

class Recipe(models.Model):
    """
    Stores a single recipe post entry related to :model:'auth.User'.
    """
    title = models.CharField(max_length=200, null=False, blank=False, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipe_poster"
    )
    description = models.CharField(max_length=400, null=False, blank=False)
    ingredients = models.TextField(null=False, blank=False)
    instructions = models.TextField(null=False, blank=False)
    image = CloudinaryField('image', null=False, blank=False)
    image_alt = models.CharField(max_length=100, null=False, blank=False)
    category = models.CharField(max_length=50, choices=CATEGORIES, default='main dishes')   
    calories = models.IntegerField()
    posted_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-posted_on"]

    def __str__(self):
        return str(self.title)
    

    
class Comment(models.Model):
    """
    Stores a single comment entry related to :model:'auth.User' and :model:'recipes.Recipe'.
    """
    post = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name= "commenter"
    )
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["created_on"]
        
    def __str__(self) :
        return f"Comment {self.body} by {self.author}"
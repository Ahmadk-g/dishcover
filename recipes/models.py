from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from cloudinary.models import CloudinaryField



# Create your models here.

# Choice Fields
CATEGORIES = (
    ('appetisers/snacks', 'Appetizers/Snacks'),
    ('beverages', 'Beverages'),
    ('soups', 'Soups'),
    ('salads', 'Salads'),
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
    likes = models.ManyToManyField(User, related_name='recipe_likes', blank=True)
    
    class Meta:
        ordering = ["-posted_on"]
        
    def total_likes(self):
        return self.likes.count()    
        
    # To ensure that the slug is always created when a new recipe is saved, whether through admin interface or form on site.
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)
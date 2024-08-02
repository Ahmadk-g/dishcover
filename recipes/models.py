from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField


MEAL_TYPE = ((0, "Breakfast"),(1, "Lunch"), (2, "Dinner"), (3, "Dessert"), (4, "Salad"), (5, "Soup"), (6, "Snack"))

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return str(self.name)
    
    def clean(self):
        # Capitalize first letter and lowercase the rest
        formatted_name = self.name.title()
        if Ingredient.objects.filter(name__iexact=formatted_name).exists():
            raise ValidationError(f"The ingredient '{formatted_name}' already exists.")
        self.name = formatted_name
        
    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method
        super().save(*args, **kwargs)


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
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    instructions = models.TextField(null=False, blank=False)
    image = CloudinaryField('image', null=False, blank=False)
    image_alt = models.CharField(max_length=100, null=False, blank=False)
    meal_type = models.IntegerField(choices=MEAL_TYPE, default=0)
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
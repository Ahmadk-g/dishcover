from django.db import models
from django.contrib.auth.models import User


STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.
class Recipe(models.Model):
    """
    Stores a single recipe post entry related to :model:'auth.User'.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipe_poster"
    )
    description = models.CharField(max_length=400, blank=True)
    calories = models.IntegerField()
    ingredients = models.TextField()
    instructions = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        ordering = ["-posted_on"]

    def __str__(self):
        return str(self.title)
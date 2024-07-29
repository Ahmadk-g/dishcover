from django.db import models
from django.contrib.auth.models import User


STATUS = ((0, "Draft"), (1, "Published"))
MEAL_TYPE = ((0, "Breakfast"),(1, "Lunch"), (2, "Dinner"), (3, "Dessert"), (4, "Salad"), (5, "Soup"), (6, "Snack"))

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
    meal_type = models.IntegerField(choices=MEAL_TYPE, default=0)
    ingredients = models.TextField()
    instructions = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
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
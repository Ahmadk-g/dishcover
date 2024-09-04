from django.db import models
from cloudinary.models import CloudinaryField  # For handling image uploads

# Create your models here.


class About(models.Model):
    """
    Stores a single 'About Me' text, including a title, content,
    an optional profile image, and the last updated timestamp.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    profile_image = CloudinaryField('image', default='placeholder')

    # Returns the title of the 'About Me' entry as its string representation
    def __str__(self):
        return self.title


class CollaborateRequest(models.Model):
    """
    Stores a single collaboration request message from a user,
    including the user's name, email, and the message content.
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)

    # Returns a string with the name of the requestor
    def __str__(self):
        return f"Collaboration request from {self.name}"

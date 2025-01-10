from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    ingredients = models.TextField(help_text="Enter ingredients each on a new line")
    instruction = models.TextField()
    cooking_time = models.IntegerField(help_text="Enter cooking time in minutes")
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True, help_text="Upload an image of the finished recipe")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.html import strip_tags
import random

# Create your models here.

STATUS = ((0, "Draft"), (1, "Published"))

class Post(models.Model):
    title = models.CharField(max_length=400, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="thread_posts")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    updated_on = models.DateTimeField(auto_now=True)
    excerpt = models.TextField(blank=True)
    tags = TaggableManager()
    category = models.CharField(max_length=100, choices=[('family', 'Family'), ('pastimes', 'Pastimes'), ('career', 'Career'), ('wall_of_complaints', 'Wall of Complaints')], default='pastimes')

    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"{self.title} | by {self.author}"
    
    def save(self, *args, **kwargs):
        self.excerpt = strip_tags(self.content[:150])
        
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_author", default=1)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"{self.body} | by {self.author}"

class User(User):
    pass


class TermsAndConditions(models.Model):
    content = models.TextField()

    def __str__(self):
        return "Terms and Conditions"

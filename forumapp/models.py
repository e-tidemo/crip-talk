from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.html import strip_tags

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

    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"{self.title} | by {self.author}"
    
    def save(self, *args, **kwargs):
        # Calculate excerpt from the first 300 characters of the content
        self.excerpt = strip_tags(self.content[:200])
        
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_author")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"{self.body} | by {self.author}"
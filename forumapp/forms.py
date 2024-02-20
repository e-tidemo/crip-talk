from django import forms
from .models import Post, Comment, User
from taggit.forms import TagField
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    """Form for adding posts"""

    tags = TagField()

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    """Form for adding comments"""

    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

#The following class is collected from reintech.io written by Arthur C. Codex - for full reference, see credits in README
class SignupForm(UserCreationForm):
    """Form for signing up for the forum"""
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


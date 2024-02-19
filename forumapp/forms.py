from django import forms
from .models import Post, Comment
from taggit.forms import TagField

class PostForm(forms.ModelForm):
    """Form for adding posts"""

    category = forms.ChoiceField(choices=[('category1', 'Category 1'), ('category2', 'Category 2'), ('category3', 'Category 3')])  # Add more choices as needed
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
from django import forms
from .models import Post, Comment, User, TermsAndConditions
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
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment'}),
        }

#The following class is collected from skolo-online.medium.com - for full reference, see credits in README
class SignupForm(UserCreationForm):
    """Form for signing up for the forum"""
    email = forms.EmailField(
    max_length=100,
    required = True,
    help_text='Enter Email Address',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    first_name = forms.CharField(
    max_length=100,
    required = True,
    help_text='Enter First Name',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
    max_length=100,
    required = True,
    help_text='Enter Last Name',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    username = forms.CharField(
    max_length=200,
    required = True,
    help_text='Enter Username',
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password1 = forms.CharField(
    help_text='Enter Password',
    required = True,
    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
    required = True,
    help_text='Enter Password Again',
    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )
    check = forms.BooleanField(required = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'check',)

class TermsAndConditionsForm(forms.ModelForm):
    class Meta:
        model = TermsAndConditions
        fields = ['content']

class ReportForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
from django import forms
from django.forms import inlineformset_factory
from .models import BlogPost, BlogImage,Comment

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['display_image','title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
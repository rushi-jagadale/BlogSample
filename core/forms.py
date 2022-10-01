from django import forms
from core.models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
    

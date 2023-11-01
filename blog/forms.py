from django import forms

from blog.models import Blog
from main.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('title', 'article', 'image')

from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    # description = forms.CharField(min_length=20)

    class Meta:
         model = Post
         fields = [
            'author',
            'postCategory',
            'title',
            'text',
            'rating',
         ]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Название новости или статьи должно начинаться с заглавной буквы"
                )
        return title

    def clean_text(self):
        text = self.cleaned_data["text"]
        if text[0].islower():
            raise ValidationError(
                "Новость и статья должна начинаться с заглавной буквы"
                )
        return text
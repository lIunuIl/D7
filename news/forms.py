from django import forms
from django.core.exceptions import ValidationError

from .models import Post, User


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'text',
            'postCategory'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if title == text:
            raise ValidationError(
                'Текст не должен быть идентичен заголовку!'
            )

        return cleaned_data


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
        ]

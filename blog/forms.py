from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Post, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags', 'og_image', 'allow_comments']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'og_image': forms.TextInput(attrs={'class': 'form-control'}),
            'allow_comments': forms.CheckboxInput(attrs={'class': 'form-check-input position-static'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Так УРЛ называть нельзя')
        return new_slug


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Так УРЛ называть нельзя')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('УРЛ должен быть уникальным. “{}” уже есть'. format(new_slug))
        return new_slug


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

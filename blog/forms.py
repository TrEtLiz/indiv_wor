from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Логин', max_length=150)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Оставьте комментарий...'}))

    class Meta:
        model = Comment
        fields = ('body',)

from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', max_length=250)
    body = forms.CharField(label='Содержимое', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('title', 'body')

from django import forms
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]

class PostForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Inserire Titolo"}))
    text = forms.CharField
    class Meta:
        model = Post
        fields = ('title', 'text',)

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        if "hack" in title or "HACK" in title or "Hack" in title:
            raise forms.ValidationError("Non puoi inserire un post che contenga 'Hack' nel titolo.")
        return title

    def clean_text(self, *args, **kwargs):
        text = self.cleaned_data.get("text")
        if "hack" in text or "HACK" in text or "Hack" in text:
            raise forms.ValidationError("Non puoi inserire un post che contenga 'Hack' nel testo.")
        return text
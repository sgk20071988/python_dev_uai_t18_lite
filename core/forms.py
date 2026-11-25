from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Message


class RegisterForm(forms.ModelForm):
    """Форма регистрации с подтверждением пароля."""
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        min_length=8,
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Форма авторизации."""
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Неверное имя пользователя или пароль.')
            cleaned_data['user'] = user
        return cleaned_data


class MessageForm(forms.ModelForm):
    """Форма отправки сообщения."""

    class Meta:
        model = Message
        fields = ['name', 'email', 'text']
        labels = {
            'name': 'Имя',
            'email': 'Email',
            'text': 'Текст сообщения',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'maxlength': 500}),
        }

    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        if not text:
            raise forms.ValidationError('Текст сообщения не может быть пустым.')
        if len(text) > 500:
            raise forms.ValidationError('Текст сообщения не должен превышать 500 символов.')
        return text
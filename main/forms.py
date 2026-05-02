from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from main.models import Profile

User = get_user_model()

class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email-адрес'
        })
    )

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    password2 = forms.CharField(
        label='Подтвердите пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.email = user.email
        if commit:
            user.save()
            if hasattr(user, 'profile'):
                user.profile.role = 'client'
                user.profile.save()
        return user

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus': True}),
        label='Ваш email',
        max_length=254,
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']

class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class FormTelegram(forms.Form):
    name = forms.CharField()
    surname = forms.CharField()
    email = forms.EmailField()
    phone = forms.NumberInput()
    text = forms.Textarea()
    class Meta:
        fields = ('name', 'surname', 'email', 'phone', 'text')
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'email': 'Email адрес',
            'phone': 'Номер телефона',
            'text': 'Сообщение',
        }
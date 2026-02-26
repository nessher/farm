from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from main.models import Profile


# class ClientRegistrationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'password1', 'password2')
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_active = True
#         if commit:
#             user.save()
#         return user
User = get_user_model()

class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        labels = {
            'email': 'Ваш email адрес',
            'password1': 'Пароль',
            'password2': 'Подтвердите пароль'
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
            if hasattr(user, 'profile'):
                user.profile.role = 'client'
                user.profile.save()
        return user

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus': True}),
        label='Email',
        max_length=254,
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
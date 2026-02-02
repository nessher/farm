from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# from main.models import CustomUser


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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
            if hasattr(user, 'profile'):
                user.profile.role = 'client'
                user.profile.save()
        return user
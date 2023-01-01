from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField



User = get_user_model()


class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User


# class UserAuthForm(AuthenticationForm):
#     username = UsernameField(widget=forms.TextInput(attrs={
#                                                     'autofocus': True,
#                                                     'class': 'form-control'
#                                                     }))
#     password = forms.CharField(
#         strip=False,
#         widget=forms.PasswordInput(attrs={
#                                     'autocomplete': 'current-password',
#                                     'class': 'form-control'})
#     )



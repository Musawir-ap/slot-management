from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import CustomUser, Role
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation



class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "password", "input_type": "password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "confirm password", "input_type": "password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'email': forms.TextInput(attrs={'input_type': 'email'}),
            'username': forms.TextInput(attrs={'input_type': 'text'}),
            # 'password1': forms.TextInput(attrs={'input_type': 'password'}),
            # 'password2': forms.TextInput(attrs={'input_type': 'password'}),
        }
        
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Role.objects.get(pk='USER')
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        
        
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserCreationAdimForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('role', )
        
        
class MyAuthForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True, "input_type": 'text'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "input_type": "password"}),
    )
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password"
        ),
        'inactive': _("This account is inactive."),
    }
    

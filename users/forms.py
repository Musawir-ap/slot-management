from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm
from .models import CustomUser, Role, BaseProfile
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


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['username', 'email']
        field_classes = {"username": UsernameField}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
        
    def clean_username(self):
        username = self.cleaned_data['username']
        queryset = CustomUser.objects.exclude(pk=self.instance.pk)

        if queryset.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already in use. Please choose a different one.')

        return username


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
    
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = BaseProfile
        # fields = ['image', 'address', 'mobile_number', 'birth_date']
        fields = ['image', 'birth_date', 'address', 'pincode', 'mobile_number']
        widgets = {
            'birth_date': forms.DateInput(attrs={'input_type': 'date', "placeholder": 'birth date'}),
            'mobile_number': forms.TextInput(attrs={'input_type': 'text',"placeholder": 'mobile nubmer'}),
            'pincode': forms.NumberInput(attrs={'input_type': 'number',"placeholder": 'pincode'}),
            # 'address': forms.NumberInput(attrs={'input_type': 'textarea',"placeholder": 'pincode'}),
        }
    
    input_formats = {
            'birth_date': ['%Y-%m-%d'],     
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].widget.format = '%Y-%m-%d'


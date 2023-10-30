from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Role


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        
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
from django import forms
from .models import ClientProfile
from users.forms import ProfileUpdateForm


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['birth_date', 'address', 'pincode', 'mobile_number']
        widgets = {
            'birth_date': forms.DateInput(attrs={'input_type': 'date', "placeholder": 'birth date'}),
            'mobile_number': forms.TextInput(attrs={"placeholder": 'mobile nubmer'}),
        }

class ClientProfileUpdateForm(ProfileUpdateForm):
    class Meta(ProfileUpdateForm.Meta):
        model = ClientProfile
        # fields = '__all__'
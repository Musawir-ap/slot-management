from django import forms
from .models import Token


class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ['token_time', 'token_date', 'purpose', 'description', 'is_booked']
        widgets = {
            'token_date': forms.DateInput(attrs={'type': 'date'}),
            'token_time': forms.TimeInput(attrs={'type': 'time'}),
        }
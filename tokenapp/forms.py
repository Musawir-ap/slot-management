from django import forms
from .models import Token


class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ['token_time', 'token_date', 'purpose', 'description']
        widgets = {
            'token_date': forms.DateInput(attrs={'type': 'date', "name": 'date'}),
            'token_time': forms.TimeInput(attrs={'type': 'time', "name": 'time'}),
            # 'purpose': forms.ChoiceField(),
            'description': forms.Textarea(attrs={'input': 'textarea', "name": 'description'}),
        }
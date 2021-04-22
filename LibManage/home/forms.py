from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class PenaltyForm(forms.Form):
    penalty_amount = forms.IntegerField(label='Penalty Amount Returned: Rs')
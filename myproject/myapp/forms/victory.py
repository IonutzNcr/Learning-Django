from django import forms
from myapp.models import Victory

class VictoryForm(forms.ModelForm):
    class Meta:
        model = Victory
        fields = ['content']
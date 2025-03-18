from django import forms
from .models import Worker, User

class AddForm(forms.ModelForm):
    class Meta:
        model = Worker
        
        fields = "__all__"

class AddForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields = "__all__"

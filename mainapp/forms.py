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


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'address', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }




            
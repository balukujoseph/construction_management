from django import forms
from django.forms import ModelForm

from management.models import Client, Project, Task, Employee, Material, Equipment, Activity


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )


class ContactForm(forms.Form):
    name = forms.CharField(
        label='Full Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
    )
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    message = forms.CharField(
        label='Your Message',
        widget=forms.Textarea(attrs={
            'placeholder': 'Write your message here',
            'rows': 5,
            'cols': 40,
        })
    )


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 1}),
        }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 1}),
        }

class MaterialForm(ModelForm):  
    
    class Meta:
        model = Material
        fields = '__all__'

class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'  


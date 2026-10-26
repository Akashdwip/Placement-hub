
from django import forms
from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'full_name',
            'department',
            'graduation_year',
            'cgpa',
            'skills',
            'resume',
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. CSE',
            }),
            'graduation_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2027',
            }),
            'cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 8.50',
                'step': '0.01',
                'min': '0',
                'max': '10',
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Python, Django, SQL...',
                'rows': 4,
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf',
            }),
        }

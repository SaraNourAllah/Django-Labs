from django import forms
from .models import Courses

class CourseForm(forms.Form):
    name = forms.CharField (max_length=50 )
    image = forms.FileField ()

from django import forms
from .models import Profiles

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ('first_name', 'last_name', 'bio', 'avatar', 'course', 'year_of_study','study_level', )
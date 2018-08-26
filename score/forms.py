

from django import forms
from .models import Score

class PostForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ('name','date','score')


from django import forms
from .models import Score, Club, Location


class PostForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ('name', 'date', 'score', 'club', 'location')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['club'] = forms.ModelChoiceField(queryset=Club.objects, )
        self.fields['location'] = forms.ModelChoiceField(queryset=Location.objects)

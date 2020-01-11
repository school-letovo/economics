from django import forms

from .models import Submit

class SubmitForm(forms.ModelForm):
    class Meta:
        model = Submit
        fields = ('short_answer','solution',)

class CheckForm(forms.ModelForm):
    class Meta:
        model = Submit
        fields = ('verdict', 'teacher_comment',)
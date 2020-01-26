from django import forms

from .models import Submit, Variant

class SubmitForm(forms.ModelForm):
    variants = forms.ModelMultipleChoiceField(queryset=None)

    class Meta:
        model = Submit
        fields = ('short_answer', 'yesno_answer', 'solution', 'variants')

    def __init__(self, problem, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if problem.variants.all():
            if problem.problem_type == 3:
                self.fields['variants'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Variant.objects.filter(problem=problem))
            elif problem.problem_type == 2:
                self.fields['variants'] = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=Variant.objects.filter(problem=problem), empty_label=None)
            self.fields['variants'].label = 'Варианты ответа'
        else:
            del self.fields['variants']

        if not problem.short_answer:
            del self.fields['short_answer']

        if not problem.yesno_answer:
            del self.fields['yesno_answer']
        else:
            self.fields['yesno_answer'].empty_label=None


        if problem.problem_type in [1, 2, 3]:
            del self.fields['solution']


class CheckForm(forms.ModelForm):
    class Meta:
        model = Submit
        fields = ('verdict', 'teacher_comment',)
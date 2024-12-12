from django import forms

from .models import Submit, Variant, Source
from economics.settings import TOPIC_ROOT, SOURCE_ROOT

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
            self.fields['variants'].label = ''
        else:
            del self.fields['variants']

        if not problem.short_answer:
            del self.fields['short_answer']

        if not problem.yesno_answer:
            del self.fields['yesno_answer']
        else:
            self.fields['yesno_answer'].empty_label = None


        if problem.problem_type in [1, 2, 3, 5]:
            del self.fields['solution']

def source_admin_tree(root):
    # children should be referenced as children in model class
    try:
        result = {'object': root, 'children': []}
    except:
        result = {'object': root, 'children': []}

    children = root.children.all()
    if children:
        for child in children:
            if "адача" not in child.name:
                result['children'].append(source_admin_tree(child))

    return result


class CheckForm(forms.ModelForm):
    class Meta:
        model = Submit
        fields = ('verdict', 'teacher_comment',)
        validate = False

class ParentSourceWidget(forms.Select):
    template_name = 'problems/source_admin.html'

    def get_context(self, name, value, attrs):
        context = super(forms.Select, self).get_context(name, value, attrs)
        #context['widget']['attrs']['choices'] = ((1, 1), (2, 2))
        root = Source.objects.get(id=SOURCE_ROOT)
        context['object_list'] = source_admin_tree(root)
        #{'object': {'name': 22, 'id': 22}, 'children':[{'object': {'name': 23, 'id': 23}}, {'object': {'name': 24, 'id': 24}}]}
        return context




class SourceAdminForm(forms.ModelForm):
  class Meta:
    model = Source
    fields = ['name', 'order', 'problems', 'parent', ]
    widgets = {
      'parent': ParentSourceWidget(),
    }

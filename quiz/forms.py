from django import forms
from django.forms.widgets import RadioSelect
from django.forms import formset_factory



class MCQuestionForm(forms.Form):
    def __init__(self,mcquestion,*args, **kwargs):
        super(MCQuestionForm, self).__init__(*args, **kwargs)
        self.fields['question'] = forms.CharField(initial=mcquestion.prompt)
        self.fields['question'].widget.attrs['disabled'] = True
        choice_list = [x for x in mcquestion.get_choices_list()]
        self.fields["choices"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect)



question_type = [('Free text', 'Free text'), ('Multiple choice', 'Multiple choice')]


class QuestionForm(forms.Form):
    question_types = forms.ChoiceField(choices=question_type)

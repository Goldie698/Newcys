from django import forms
from django.forms.widgets import RadioSelect


class MCQuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(MCQuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_choices_list()]
        self.fields["choices"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect)


question_type = [('Free text', 'Free text'), ('Multiple choice', 'Multiple choice')]


class QuestionForm(forms.Form):
    question_types = forms.ChoiceField(choices=question_type)

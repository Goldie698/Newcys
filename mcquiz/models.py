from django.db import models
from quiz.models import Question
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class MCQuestion(Question):

    def check_if_correct(self, guess):
        answer = Choice.objects.get(id=guess)
        if answer.choice_text == self.answer:
            return True
        else:
            return False

    def get_choices_list(self):
        return [(choice.id, choice.choice_text) for choice in
                Choice.objects.filter(question=self)]

    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")


class Choice(models.Model):
    question = models.ForeignKey(MCQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text

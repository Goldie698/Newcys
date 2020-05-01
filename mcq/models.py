from django.db import models

# Create your models here.
from django.db import models
from quiz.models import Round
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class MCQuestion(models.Model):
    prompt = models.CharField(max_length=300)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

    def check_if_correct(self, guess):
        answer = Choice.objects.get(id=guess)
        if answer.correct:
            return True
        else:
            return False

    def get_choices_list(self):
        return [(choice.id, choice.choice_text) for choice in
                Choice.objects.filter(question=self)]

    def __str__(self):
        return self.prompt

    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")


class Choice(models.Model):
    question = models.ForeignKey(MCQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    correct = models.BooleanField(blank=False,
                                  default=False,
                                  help_text=_("Is this a correct answer?"),
                                  verbose_name=_("Correct"))

    def __str__(self):
        return self.choice_text

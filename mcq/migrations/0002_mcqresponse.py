# Generated by Django 3.0.5 on 2020-05-01 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_quiztakers_response'),
        ('mcq', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MCQResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcq.MCQuestion')),
                ('quiztaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.QuizTakers')),
            ],
        ),
    ]

# Generated by Django 3.0.5 on 2020-04-20 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_remove_quiz_numqs'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='numqs',
            field=models.IntegerField(default=0),
        ),
    ]

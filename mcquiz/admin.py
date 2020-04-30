from django.contrib import admin
from .models import MCQuestion, Choice
# Register your models here.
admin.site.register(MCQuestion),
admin.site.register(Choice)
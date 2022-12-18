from django.contrib import admin

from .models import Question, Players

# Register your models here.
admin.site.register(Question)
admin.site.register(Players)
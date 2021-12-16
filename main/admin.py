from django.contrib import admin

from main import models


admin.site.register(models.QuizResult)
admin.site.register(models.Quiz)
admin.site.register(models.Question)
admin.site.register(models.Category)


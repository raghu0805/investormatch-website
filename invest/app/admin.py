from django.contrib import admin
from .models import Question,Question1,UserScore,CustomUser

admin.site.register(Question)
admin.site.register(Question1)
admin.site.register(UserScore)
admin.site.register(CustomUser)
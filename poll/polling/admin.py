from django.contrib import admin
from .models import User, Question, Votes
# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Votes)
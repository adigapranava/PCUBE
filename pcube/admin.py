from django.contrib import admin
from .models import Post, Buy, Notification, Question, Answer

# Register your models here.
admin.site.register(Post)
admin.site.register(Buy)
admin.site.register(Notification)
admin.site.register(Answer)
admin.site.register(Question)

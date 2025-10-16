from django.contrib import admin
from .models import ReactionModel,CommentModel
# Register your models here.
admin.site.register(ReactionModel)
admin.site.register(CommentModel)

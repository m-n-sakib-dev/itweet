from django.contrib import admin
from .models import UserProfile,SavedTweet,FollowModel
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(SavedTweet)
admin.site.register(FollowModel)


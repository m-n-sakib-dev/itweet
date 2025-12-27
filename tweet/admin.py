from django.contrib import admin
from .models import Tweet,TweetModel,Hashtag,TrendingHashtag
# Register your models here.

admin.site.register(Tweet)
admin.site.register(TweetModel)
admin.site.register(Hashtag)
admin.site.register(TrendingHashtag)
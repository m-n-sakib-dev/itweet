from django.contrib import messages
from django.shortcuts import render
from ..models import Tweet,TweetModel



def tweet_feed_global(request):
    tweets = TweetModel.objects.all().order_by('-created_at')
    return render(request, 'tweet_feed.html', {'tweets': tweets})

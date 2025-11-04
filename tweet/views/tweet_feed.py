from django.contrib import messages
from django.shortcuts import render
from ..models import Tweet,TweetModel
from interactions.forms import CommentForm



def tweet_feed_global(request):
    tweets = TweetModel.objects.all().order_by('-created_at')
    comment_form=CommentForm()
    return render(request, 'tweet_feed.html', {'tweets': tweets, 'comment_form':comment_form,'text':tweets[0].text})

def tweet_list(tweets):
    for tweet in tweets:
        pass
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from ..models import Tweet,TweetModel
from interactions.models import ReactionModel
from interactions.forms import CommentForm



def tweet_feed_global(request):
    tweets = TweetModel.objects.all()
    comment_form=CommentForm()
    if request.user.is_authenticated:
        reactions=ReactionModel.objects.filter(user=request.user)
    return render(request, 'tweet_feed.html', {'tweets': tweets, 'comment_form':comment_form,'text':tweets[0].text})

def feedTweets(request):
        tweets=TweetModel.objects.all()
        tweetList=list(tweets.values())
        for tweet,tweet_data in zip(tweetList,tweets):
                tweet['user']={'username':tweet_data.user.username}
                tweet['photo']={'url':tweet_data.photo.url}
        print(tweets)
        return JsonResponse({
                'success': True,
                'tweets':tweetList,
        })
        
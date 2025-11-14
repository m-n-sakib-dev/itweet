from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from ..models import TweetModel
from interactions.models import ReactionModel
from interactions.forms import CommentForm
from django.contrib.auth.decorators import login_required



def tweet_feed_global(request):
        comment_form=CommentForm()
        functiontocall='loadTweets(1)'
        return render(request, 'tweet_feed.html', {'comment_form':comment_form,'load_tweet_function':functiontocall,'call_from':"tweet_global_feed"})

# def feedTweets(request):
#         tweets=TweetModel.objects.all()
#         tweetList=list(tweets.values())
#         for tweet,tweet_data in zip(tweetList,tweets):
#                 tweet['user']={'username':tweet_data.user.username}
#                 tweet['photo']={'url':tweet_data.photo.url}
#         print(tweets)
#         return JsonResponse({
#                 'success': True,
#                 'tweets':tweetList,
#         })

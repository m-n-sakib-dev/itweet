from django.shortcuts import get_object_or_404,redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from tweet.models import TweetModel
from interactions.models import ReactionModel
from django.contrib.auth.models import User
from django.core.serializers import serialize
from interactions.forms import CommentForm
from ..models import UserProfile as UserProfileModel,SavedTweet
from django.forms.models import model_to_dict
from tweet.views import tweetAllData

tweet_per_page=2

@login_required
def UserTweets(request):
        profile_id=request.GET.get('user_id')
        page=int(request.GET.get('page','1'))
        start=tweet_per_page*(page-1)
        end=tweet_per_page*page
        user=request.user
        profile_owner=get_object_or_404(User,id=profile_id)
        tweets=TweetModel.objects.filter(user=profile_owner).select_related('user__profile')[start:end]
        tweets_data = tweetAllData(tweets,user)         
        return JsonResponse({
                'success': True,
                'tweets':tweets_data,
                'is_more': len(tweets_data)==tweet_per_page
        })


@login_required
def SaveTweet(request,tweet_id):
    if request.user.is_authenticated:
        if request.method=='POST':
            tweet = get_object_or_404(TweetModel, id=tweet_id)
            try:
                if not SavedTweet.objects.filter(user=request.user, tweet=tweet).exists():
                    save_tweet = SavedTweet.objects.create(user=request.user, tweet=tweet)
                    return JsonResponse({'success': True, 'message': 'Tweet saved'})
                else:
                    saved_tweet=SavedTweet.objects.get(user=request.user, tweet=tweet)
                    saved_tweet.delete()
                    return JsonResponse({'success': True, 'message': 'Tweet unsaved'})
            except TweetModel.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Tweet not found'})
        
@login_required
def SavedTweetsPage(request):
        user=request.user
        if user.is_authenticated:
                comment_form=CommentForm()
                functiontocall='loadTweets(1)'
                return render(request, 'tweet_feed.html', {'comment_form':comment_form,'load_tweet_function':functiontocall,'call_from':"Saved Tweets"})

@login_required
def SavedTweets(request):
        pass

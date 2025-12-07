from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from ..models import TweetModel
from user_profile.models import  SavedTweet,FollowModel
from interactions.models import ReactionModel
from interactions.forms import CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .hashtag import Hastagify



def tweet_feed_global(request):
        comment_form=CommentForm()
        functiontocall='loadTweets(1)'
        return render(request, 'tweet_feed.html', {'comment_form':comment_form,'load_tweet_function':functiontocall,'call_from':"tweet_global_feed"})

tweet_per_page=10

def GolobalTweetLoad(request):
        page=int(request.GET.get('page'))
        start=tweet_per_page*(page-1)
        end=tweet_per_page*page
        if request.user.is_authenticated:
                user=request.user
        else:
                user=None
        tweets=TweetModel.objects.all().select_related('user__profile')[start:end]
        tweets_data = tweetAllData(tweets,user)         
        return JsonResponse({
                'success': True,
                'tweets':tweets_data,
                'is_more': len(tweets_data)==tweet_per_page
        })
def tweetAllData(tweets,user):
        tweets_data=[]
        for tweet in tweets:
                data = model_to_dict(tweet)
                data['text']=Hastagify(tweet.text)
                del data["hashtags"]
                data['reaction']=ReactionModel.objects.filter(user=user,tweet=tweet).values_list('reactiontype', flat=True).first()
                data['is_saved']=SavedTweet.objects.filter(user=user,tweet=tweet).exists()
                data['photo'] = {'url': tweet.photo.url}   if tweet.photo else None
                data['created_at']=tweet.created_at.strftime("%b %d, %Y at %I:%M %p")
                data['user'] = model_to_dict(tweet.user,fields=['id','username'])
                data['user']['profile'] = model_to_dict(tweet.user.profile,fields=['name','follower_count','following_count'])  
                data['user']['profile']['profile_picture'] = tweet.user.profile.profile_picture.url
                data['user']['profile']['cover_photo'] = tweet.user.profile.cover_photo.url
                data['user']['profile']['is_following']=FollowModel.objects.filter(user=user,following_to=tweet.user).exists()
                tweets_data.append(data)
        return tweets_data



@login_required
def FollowingTweetLoad(request):
        page=int(request.GET.get('page'))
        start=tweet_per_page*(page-1)
        end=tweet_per_page*page
        if request.user.is_authenticated:
                user=request.user
        else:
                return JsonResponse({
                'success': False,
        })
        following_users=FollowModel.objects.filter(user=user).values_list('following_to__id', flat=True)
        tweets=TweetModel.objects.filter(user__id__in=following_users).select_related('user__profile')[start:end]
        tweets_data = tweetAllData(tweets,user)         
        return JsonResponse({
                'success': True,
                'tweets':tweets_data,
                'is_more': len(tweets_data)==tweet_per_page
        })



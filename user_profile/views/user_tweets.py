from django.shortcuts import get_object_or_404,redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from tweet.models import TweetModel
from interactions.models import ReactionModel
from django.contrib.auth.models import User
from django.core.serializers import serialize
from interactions.forms import CommentForm
from django.contrib import messages
from ..models import UserProfile as UserProfileModel,SavedTweet
from ..forms import UserUpdateForm, UserProfileUpdateForm
from django.forms.models import model_to_dict


@login_required
def UserTweets(request):
        user_id=request.GET.get('user_id')
        user=get_object_or_404(User,id=user_id)
        author_profile=UserProfileModel.objects.get(user=user)
        author=serialize('python',[author_profile])
        author=author[0]['fields']
        author.update({'profile_picture_url':author_profile.profile_picture.url})
        tweets=TweetModel.objects.filter(user=user)
        tweetList=list(tweets.values())
        for tweet,tweet_data in zip(tweetList,tweets):
                tweet['user']={'username':author_profile.user.username}
                tweet['author']=author
                tweet['created_at']=tweet_data.created_at.strftime("%b %d, %Y at %I:%M %p")
                tweet['reaction']= ReactionModel.objects.filter(user=user,tweet=tweet_data).values_list('reactiontype', flat=True).first()
                tweet['is_saved']= SavedTweet.objects.filter(user=user,tweet=tweet_data).exists()
                if(tweet_data.photo):
                    tweet['photo']={'url':tweet_data.photo.url}
        return JsonResponse({
                'success': True,
                'tweets':tweetList,
        })

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
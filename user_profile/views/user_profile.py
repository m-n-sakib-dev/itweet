from django.shortcuts import get_object_or_404,redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from tweet.models import TweetModel
from django.contrib.auth.models import User
from django.core.serializers import serialize
from interactions.forms import CommentForm
from django.contrib import messages
from ..models import UserProfile as UserProfileModel
from ..forms import UserUpdateForm, UserProfileUpdateForm
from django.forms.models import model_to_dict

def UserProfile(request,user_id):
        user=get_object_or_404(User,id=user_id)
        user_profile=get_object_or_404(UserProfileModel,user=user)
        comment_form=CommentForm()
        return render(request, 'user_profile.html',{'comment_form':comment_form, "profile_user_id":user_id,'user_profile':user_profile})

def UserTweets(request):
        user_id=request.GET.get('user_id')
        user=get_object_or_404(User,id=user_id)
        user_profile=UserProfileModel.objects.get(user=user)
        author=serialize('python',[user_profile])
        author=author[0]['fields']
        author.update({'profile_picture_url':user_profile.profile_picture.url})
        tweets=TweetModel.objects.filter(user=user)
        tweetList=list(tweets.values())
        for tweet,tweet_data in zip(tweetList,tweets):
                tweet['user']={'username':user.username}
                tweet['author']=author
                if(tweet_data.photo):
                    tweet['photo']={'url':tweet_data.photo.url}
        return JsonResponse({
                'success': True,
                'tweets':tweetList,
        })
        



@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    
    # Check if profile is public or user is viewing their own profile
    if not profile.is_profile_public and request.user != user:
        messages.warning(request, "This profile is private.")
        return redirect('home')
    
    context = {
        'profile_user': user,
        'profile': profile,
    }
    return render(request, 'users/profile.html', context)

@login_required
def EditProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user_profile', user_id=request.user.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Edit Profile'
    }
    return render(request, 'edit_profile.html', context)
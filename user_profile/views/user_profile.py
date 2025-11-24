from django.shortcuts import get_object_or_404,redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from tweet.models import TweetModel
from django.contrib.auth.models import User
from django.core.serializers import serialize
from interactions.forms import CommentForm
from django.contrib import messages
from ..models import UserProfile as UserProfileModel,SavedTweet
from ..forms import UserUpdateForm, UserProfileUpdateForm
from django.forms.models import model_to_dict

@login_required
def UserProfile(request,user_id):
        user=get_object_or_404(User,id=user_id)
        user_profile=get_object_or_404(UserProfileModel,user=user)
        comment_form=CommentForm()
        return render(request, 'user_profile.html',{'comment_form':comment_form, "profile_user_id":user_id,'user_profile':user_profile})

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



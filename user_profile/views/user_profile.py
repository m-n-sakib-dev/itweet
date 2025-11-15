from django.shortcuts import get_object_or_404,redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from tweet.models import TweetModel
from django.contrib.auth.models import User
from django.core.serializers import serialize
from interactions.forms import CommentForm
from django.contrib import messages
from ..models import UserProfile as UserProfileModel,FollowModel
from ..forms import UserUpdateForm, UserProfileUpdateForm
from django.forms.models import model_to_dict

@login_required
def UserProfile(request,user_id):
        user=get_object_or_404(User,id=user_id)
        user_profile=get_object_or_404(UserProfileModel,user=user)
        comment_form=CommentForm()
        is_following=FollowModel.objects.filter(user=request.user,following_to=user).exists()
        return render(request, 'user_profile.html',{
            'comment_form':comment_form, 
            "profile_user":user,
            'user_profile':user_profile,
            'is_following':is_following,
            })



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
def FollowUser(request,to_follow_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User, id=to_follow_id)
        
        # Check if already following
        is_following = FollowModel.objects.filter(
            user=request.user, 
            following_to=target_user
        ).exists()
        
        if is_following:
            # Unfollow
            FollowModel.objects.get(
                user=request.user, 
                following_to=target_user
            ).delete()
            action = 'unfollowed'
        else:
            # Follow
            FollowModel.objects.create(
                user=request.user, 
                following_to=target_user
            )
            action = 'followed'
        
        # Get updated counts
        followers_count = target_user.profile.follower_count
        following_count = target_user.profile.following_count
        my_following_count=request.user.profile.following_count
        return JsonResponse({
            'success': True,
            'action': action,
            'followers_count': followers_count,
            'following_count': following_count,
            'user_following_count':my_following_count,
            'is_following': not is_following
        })
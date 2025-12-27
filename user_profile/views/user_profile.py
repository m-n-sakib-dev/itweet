from django.shortcuts import get_object_or_404,redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from tweet.models import TweetModel
from django.contrib.auth.models import User
from interactions.forms import CommentForm
from django.contrib import messages
from ..models import UserProfile as UserProfileModel,FollowModel
from ..forms import UserUpdateForm, UserProfileUpdateForm
from django.forms.models import model_to_dict
from django.template.loader import render_to_string


@login_required
def UserProfile(request,user_id):
        user=get_object_or_404(User,id=user_id)
        user_profile=get_object_or_404(UserProfileModel,user=user)
        comment_form=CommentForm()
        is_following=FollowModel.objects.filter(user=request.user,following_to=user).exists() if request.user.is_authenticated else False
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

def BasicProfile(request,profile):
    return{
        'id':profile.user.id,
        'name':profile.name,
        'username':profile.user.username,
        'profile_picture':profile.profile_picture.url,
        'cover_photo':profile.cover_photo.url,
        'follower_count':profile.follower_count,
        'following_count':profile.following_count,
        'is_following': FollowModel.objects.filter(
            user=request.user, 
            following_to=profile.user
        ).exists() if request.user.is_authenticated else False
    }
    
def ProfileAbout(request,user_id):
        user=get_object_or_404(User,id=user_id)
        user_profile=get_object_or_404(UserProfileModel,user=user)
        about_content = render_to_string('user_profile_right_panel.html', model_to_dict(user_profile))
        return JsonResponse({'about_content': about_content})
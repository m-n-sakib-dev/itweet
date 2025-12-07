from django.shortcuts import get_object_or_404,redirect, render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from ..models import UserProfile as UserProfileModel,FollowModel
from django.forms.models import model_to_dict
from .user_profile import BasicProfile
from django.urls import reverse
from functools import wraps


def login_required_redirect(view_func):
    """Decorator that redirects ALL requests (including AJAX) to login"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = reverse('login')  # Use your login URL name
            next_url = request.get_full_path()
            redirect_url = f"{login_url}?next={next_url}"
            is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
            
            if is_ajax:
                # For AJAX: Return JSON that tells JavaScript to redirect
                print("Redirecting AJAX request to login")
                return JsonResponse({
                    'success': False,
                    'redirect': True,
                    'redirect_url': redirect_url,
                    'message': 'Please login to continue'
                }, status=403)
            else:
                # For regular requests: Use Django's redirect
                print("Redirecting regular request to login")
                return HttpResponseRedirect(redirect_url)
        
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_redirect
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
        
def FollowSuggestion(request):
        if not request.user.is_authenticated:
                most_follower=UserProfileModel.objects.all().order_by('-follower_count')[:10]
                suggested_users=most_follower
        else:
                user=request.user
                suggested_users=UserProfileModel.objects.exclude(user__in=user.following.values_list('following_to', flat=True)).exclude(user=user).order_by('-follower_count')[:10]
        
        suggested_users_list=[]
        for profile in suggested_users:
                suggested_users_list.append(BasicProfile(request,profile))
        return JsonResponse({
		'success':True,
		'suggested_users':suggested_users_list,
        })
        
def userFollowersList(request,profile_id):
        profile=User.objects.get(id=profile_id)
        # follower_users=profile.follower.all()
        follower_users=UserProfileModel.objects.filter(user__following__following_to=profile)
        follower_user_list=[]
        for profile in follower_users:
            follower_user_list.append(BasicProfile(request,profile))
        return JsonResponse({
            'success':True,
            'list':follower_user_list
            })

def userFollowingList(request,profile_id):
        profile=User.objects.get(id=profile_id)
        # following_users=profile.following.all()
        following_users=UserProfileModel.objects.filter(user__follower__user=profile)
        following_user_list=[]
        for profile in following_users:
            following_user_list.append(BasicProfile(request,profile))
        return JsonResponse({
            'success':True,
            'list':following_user_list
            })
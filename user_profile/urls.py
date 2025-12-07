from django.urls import path
from .views import UserProfile,UserTweets,EditProfile,SaveTweet,FollowUser,FollowSuggestion,ProfileAbout
from .views import userFollowersList,userFollowingList
from django.contrib.auth import views as auth_views

urlpatterns = [
#     path("admin/", admin.site.urls),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('profile/<int:user_id>', UserProfile, name='user_profile'),
	path('profile/tweets', UserTweets, name='user_tweets'),
	path('profile/edit-profile/', EditProfile, name='edit_profile'),
	path('tweet/<int:tweet_id>/save', SaveTweet, name='save_tweets'),
	path('profile/<int:to_follow_id>/togglefollow', FollowUser, name='follow_user'),
	path('profile/<int:user_id>/about', ProfileAbout, name='user_profile_about'),
	path('profile/<int:profile_id>/followers', userFollowersList, name='user_profile_follower'),
	path('profile/<int:profile_id>/following', userFollowingList, name='user_profile_following'),
]
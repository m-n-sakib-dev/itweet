from django.urls import path
from .views import (
    UserProfile,
    UserTweets,
    EditProfile,
    SaveTweet,
    FollowUser,
    ProfileAbout,
    userFollowersList,
    userFollowingList,
    SavedTweetsPage,
    SavedTweets,
    verify_email_page,
    resend_verification_code,
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    #     path("admin/", admin.site.urls),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/<int:user_id>", UserProfile, name="user_profile"),
    path("profile/tweets", UserTweets, name="user_tweets"),
    path("profile/edit-profile/", EditProfile, name="edit_profile"),
    path("tweet/<int:tweet_id>/save", SaveTweet, name="save_tweets"),
    path("profile/<int:to_follow_id>/togglefollow", FollowUser, name="follow_user"),
    path("profile/<int:user_id>/about", ProfileAbout, name="user_profile_about"),
    path(
        "profile/<int:profile_id>/followers",
        userFollowersList,
        name="user_profile_follower",
    ),
    path(
        "profile/<int:profile_id>/following",
        userFollowingList,
        name="user_profile_following",
    ),
    path("saved-tweets-page", SavedTweetsPage, name="user_saved_tweets_page"),
    path("saved-tweets", SavedTweets, name="user_saved_tweets"),
    path("verify-email/", verify_email_page, name="verify_email_page"),
    path("resend-code/", resend_verification_code, name="resend_code"),
]

from django.urls import path
from .views import tweet_feed_global,CreateTweet,tweet_delete,TweetEdit,Home,GolobalTweetLoad,FollowingTweetLoad,getTrendingHashtag
from django.contrib.auth import views as auth_views

urlpatterns = [
#     path("admin/", admin.site.urls),
	path('',Home,name='home'),
	path('tweets/home/all',GolobalTweetLoad,name='all_tweets'),
	path('tweets/home/following_tweets',FollowingTweetLoad,name='following_tweets'),
	path('tweet_create/',CreateTweet,name='tweet_create'),
	path('tweet_edit/<int:tweet_id>',TweetEdit,name='tweet_edit'),
	path('tweet_delete/<int:tweet_id>',tweet_delete,name='tweet_delete'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('tweet_feed/',Home,name='tweet_feed'),
	path('hastags/trending-hashtags',getTrendingHashtag,name='trending_hashtags'),
]
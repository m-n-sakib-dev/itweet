from django.urls import path
from .views import tweet_feed_global,CreateTweet,tweet_delete,TweetEdit,Home,GolobalTweetLoad,FollowingTweetLoad
from .views import Search,getTrendingHashtag,HashtagTweetsPage,HashtagTweets
from django.contrib.auth import views as auth_views
from .services import update_trending_table


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
	path('search/',Search,name='search'),
	path('hastags/<str:hashtag_name>/hashtag_page',HashtagTweetsPage,name='hashtag_page'),
	path('hastags/<str:hashtag_name>/tweets',HashtagTweets,name='hashtag_tweets'),
	path('hastags/update-trending',update_trending_table,name='update_trending'),
 
]
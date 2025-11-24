from django.urls import path
from .views import tweet_feed_global,CreateTweet,tweet_delete,TweetEdit
from django.contrib.auth import views as auth_views

urlpatterns = [
#     path("admin/", admin.site.urls),
	
	path('',tweet_feed_global,name='tweet_feed'),
	path('tweet_create/',CreateTweet,name='tweet_create'),
	path('tweet_edit/<int:tweet_id>',TweetEdit,name='tweet_edit'),
	path('tweet_delete/<int:tweet_id>',tweet_delete,name='tweet_delete'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('tweet_feed/',tweet_feed_global,name='tweet_feed'),
]
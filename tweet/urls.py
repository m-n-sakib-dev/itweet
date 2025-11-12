from django.urls import path
from .views import views,tweet_feed_global,CreateTweet
from django.contrib.auth import views as auth_views

urlpatterns = [
#     path("admin/", admin.site.urls),
	
	path('',tweet_feed_global,name='tweet_feed'),
	path('tweet_list/',views.tweet_list,name='tweet_list'),
	path('tweet_create/',CreateTweet,name='tweet_create'),
	path('<int:tweet_id>/tweet_edit/',views.tweet_edit,name='tweet_edit'),
	path('<int:tweet_id>/tweet_delete/',views.tweet_delete,name='tweet_delete'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('tweet_feed/',tweet_feed_global,name='tweet_feed'),
]
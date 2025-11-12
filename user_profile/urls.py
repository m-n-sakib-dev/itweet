from django.urls import path
from .views import UserProfile,UserTweets,EditProfile
from django.contrib.auth import views as auth_views

urlpatterns = [
#     path("admin/", admin.site.urls),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('profile/<int:user_id>', UserProfile, name='user_profile'),
	path('profile/tweets', UserTweets, name='user_tweets'),
	path('profile/edit-profile/', EditProfile, name='edit_profile'),
]
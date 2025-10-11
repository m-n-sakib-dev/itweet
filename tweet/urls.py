from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
#     path("admin/", admin.site.urls),
	path('', views.index, name='index'),
	path('tweet_list/',views.tweet_list,name='tweet_list'),
	path('tweet_create/',views.tweet_create,name='tweet_create'),
	path('<int:tweet_id>/tweet_edit/',views.tweet_edit,name='tweet_edit'),
	path('<int:tweet_id>/tweet_delete/',views.tweet_delete,name='tweet_delete'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
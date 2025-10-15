from django.urls import path
from .views import GiveReaction
from django.contrib.auth import views as auth_views

urlpatterns = [

	path('<int:tweet_id>/reaction/<str:reaction_type>',GiveReaction,name='give_reaction'),
	
]
from django.contrib import messages
from django.shortcuts import render
from tweet.models import TweetModel
from ..models import ReactionModel
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.http import JsonResponse

@login_required
def makeComment(request,tweet_id):
	tweet=get_object_or_404(TweetModel,id=tweet_id)
	if request.method=='POST':
		pass
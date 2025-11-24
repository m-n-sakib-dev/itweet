from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from ..models import TweetModel
from interactions.models import ReactionModel
from interactions.forms import CommentForm
from django.contrib.auth.decorators import login_required

def Home(request):
        # comment_form=CommentForm()
        functiontocall='loadTweets(1)'
        return render(request, 'home.html', {'load_tweet_function':functiontocall,'call_from':"home"})

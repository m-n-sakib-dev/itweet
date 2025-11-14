from django.shortcuts import get_object_or_404, redirect, render
from ..models import TweetModel
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(TweetModel,pk=tweet_id)
    user=tweet.user
    if request.user==user:
        if request.method=='POST':
            try:
                tweet.delete()
                return JsonResponse({
                    'success':True
                })
            except Exception as e:
                return JsonResponse({
                    'error':e
                })
    else:
        return JsonResponse({
            'warning': True
        })
from django.contrib import messages
from django.shortcuts import render
from tweet.models import TweetModel
from ..models import ReactionModel
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.http import JsonResponse

@login_required
def GiveReaction(request,tweet_id,reaction_type):
        tweet=get_object_or_404(TweetModel,id=tweet_id)      
        reaction, created = ReactionModel.objects.get_or_create(
        user=request.user,
        tweet=tweet,
        defaults={'reactiontype': reaction_type}
    	)
        if not created:
            if reaction.reactiontype==reaction_type:
                  reaction.delete()
            else:
                reaction.reactiontype=reaction_type
                reaction.save()
        tweet.update_reaction_count()      
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'like_count': tweet.like_count,'unlike_count':tweet.unlike_count,'tweet_id':tweet.id})
        
        return redirect('tweet_feed')
    

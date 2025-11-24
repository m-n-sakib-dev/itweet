from django.contrib import messages
from django.shortcuts import render
from tweet.models import TweetModel
from interactions.models import CommentModel,CommentLike
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..forms import CommentForm


@login_required
def addComment(request, tweet_id):
    tweet = get_object_or_404(TweetModel, id=tweet_id)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.tweet= tweet
            comment.user = request.user
            comment.save()
            returncomment=commentInfo(comment)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment_id': comment.id,
                    'comment_count':tweet.comment_count,
                    'comment_data':returncomment
                })
           
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	return JsonResponse({'success': False, 'errors': comment_form.errors})

def Comments_list(request,tweet_id):
    if request.method=='POST':
        tweet=get_object_or_404(TweetModel,id=tweet_id)
        comments=tweet.comments.filter(parent=None)
        # sending full html response. 
        # comment_html=render_to_string('components/comment_body.html',{'comments':comments})
        comments_list=[]
        for comment in comments:
            comment_info=commentInfo(comment)
            comments_list.append(comment_info)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success':True,'comments_list':comments_list})
        
def ReplyComments_list(request,comment_id):
    if request.method=='POST':
        comment=get_object_or_404(CommentModel,id=comment_id)
        comments=CommentModel.objects.filter(parent=comment)
        # sending full html response. 
        # comment_html=render_to_string('components/comment_body.html',{'comments':comments})
        comments_list=[]
        for comment in comments:
            comment_info=commentInfo(comment)
            comments_list.append(comment_info)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success':True,'comments_list':comments_list})

def commentInfo(comment):
    if not comment:
        return comment
    return {
                'id':comment.id,
                'tweet_id':comment.tweet.id,
                'content':comment.content,
                'user':{
                    'user_id':comment.user.id,
                    'user_name':comment.user.username,
                    },
                'like_count':comment.like_count,
                'unlike_count':comment.unlike_count,
                'reply_count':comment.reply_count,
                
                }
        
@login_required
def CommentReaction(request,comment_id,reaction_type):
        comment=get_object_or_404(CommentModel,id=comment_id)      
        reaction, created = CommentLike.objects.get_or_create(
        user=request.user,
        comment=comment,
        defaults={'reactiontype': reaction_type}
    	)
        if not created:
            if reaction.reactiontype==reaction_type:
                  reaction.delete()
            else:
                reaction.reactiontype=reaction_type
                reaction.save()
        comment.update_reaction_count()      
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'like_count': comment.like_count,'unlike_count':comment.unlike_count,'comment_id':comment.id,'rtweet_id':reaction.comment.id})
        
        return redirect('tweet_feed')
    
@login_required
def CommentReply(request,comment_id):
    parent_comment=get_object_or_404(CommentModel,id=comment_id)
    tweet = parent_comment.tweet
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.tweet= tweet
            comment.user = request.user
            comment.parent=parent_comment
            comment.save()
            returncomment=commentInfo(comment)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment_id': comment.id,
                    'tweet_id':tweet.id,
                    'comment_count':tweet.comment_count,
                    'comment_data':returncomment,
                    'reply_count':parent_comment.reply_count,
                })
            messages.success(request, 'Comment added successfully!')
           
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	return JsonResponse({'success': False, 'errors': comment_form.errors})


def CommentsReply_list(request,comment_id):
    if request.method=='POST':
        parent_comment=get_object_or_404(CommentModel,id=comment_id)
        comments=parent_comment.replies.all()
        # sending full html response. 
        # comment_html=render_to_string('components/comment_body.html',{'comments':comments})
        comments_list=[]
        for comment in comments:
            comment_info=commentInfo(comment)
            comments_list.append(comment_info)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success':True,'comments_list':comments_list})
        
@login_required
def DeleteComment(request,comment_id):
    if request.method=='POST':
        comment=get_object_or_404(CommentModel,id=comment_id)
        
        if request.user==comment.user:
            tweet=comment.tweet
            parent=comment.parent
            try:
                comment.delete()
                if not parent:
                    parent=parent.update()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success':True,"tweet_id":tweet.id,"tweet_comment_count":tweet.comment_count,"parent":commentInfo(parent)})
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success':False,'error':e})


@login_required
def EditComment(request,comment_id):
    comment=get_object_or_404(CommentModel,id=comment_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment.content=request.POST['content']
            comment.save()
            returncomment=commentInfo(comment)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment_id': comment.id,
                    'comment_data':returncomment
                })
            messages.success(request, 'Comment added successfully!')
           
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	return JsonResponse({'success': False, 'errors': comment_form.errors})
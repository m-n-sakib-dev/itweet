from django.urls import path
from .views import GiveReaction,addComment,Comments_list,CommentReaction,CommentReply,CommentsReply_list,DeleteComment,EditComment
from django.contrib.auth import views as auth_views

urlpatterns = [

	path('<int:tweet_id>/reaction/<str:reaction_type>',GiveReaction,name='give_reaction'),
 	path('<int:tweet_id>/comment/',addComment,name='add_comment'),
	path('<int:tweet_id>/comments_list/',Comments_list,name='comment_list'),
	path('comment/<int:comment_id>/reaction/<str:reaction_type>',CommentReaction,name='comment_rection'),
	path('comments/<int:comment_id>/comment_reply/',CommentReply,name='reply_comment'),
	path('comments/<int:comment_id>/replies/',CommentsReply_list,name='reply_comment_list'),
	path('comments/<int:comment_id>/delete/',DeleteComment,name='delete_comment'),
	path('comments/<int:comment_id>/edit/',EditComment,name='edit_comment'),
 
]
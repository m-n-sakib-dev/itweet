from django.db import models
from django.contrib.auth.models import User
from tweet.models import TweetModel

class ReactionModel(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	tweet=models.ForeignKey(TweetModel, on_delete=models.CASCADE)
	reactiontype= models.CharField(max_length=6)
	class Meta:
		unique_together = ['user','tweet','reactiontype']
		indexes=[
			models.Index(fields=['user','tweet']),
			models.Index(fields=['tweet','reactiontype'])
		]

	def save(self,*args, **kwargs):
		super().save(*args, **kwargs)
		self.tweet. update_reaction_count()
	def delete(self, *args, **kwargs):
		tweet=self.tweet
		super().delete(*args, **kwargs)
		tweet. update_reaction_count()
  

class CommentModel(models.Model):
	tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	parent = models.ForeignKey(
		'self', 
		on_delete=models.CASCADE, 
		null=True, 
		blank=True, 
		related_name='replies'
	)
	content = models.TextField(max_length=500)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	likes_count = models.IntegerField(default=0)
	unlike_count=models.IntegerField(default=0)
	
	class Meta:
		ordering = ['created_at']
		indexes = [
		models.Index(fields=['tweet', 'created_at']),
		]
	
	def update_likes_count(self):
		# self.likes_count = self.comment_likes.count()
		self.save()
	
	def is_reply(self):
		return self.parent is not None
	
	def __str__(self):
		return f" {self.author.username} commented on {self.post.id}"

# class CommentLike(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
#     created_at = models.DateTimeField(auto_now_add=True)
#     reactiontype= models.CharField(max_length=6)
#     class Meta:
#         unique_together = ['user', 'comment']
#         indexes = [
#             models.Index(fields=['user', 'comment']),
#             models.Index(fields=['comment', 'created_at']),
#         ]
    
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.comment.update_likes_count()
    
#     def delete(self, *args, **kwargs):
#         comment = self.comment
#         super().delete(*args, **kwargs)
#         comment.update_likes_count()
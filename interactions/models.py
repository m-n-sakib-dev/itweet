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
	like_count = models.IntegerField(default=0)
	unlike_count=models.IntegerField(default=0)
	reply_count=models.IntegerField(default=0)
	
	class Meta:
		ordering = ['-created_at']
		indexes = [
		models.Index(fields=['tweet', 'created_at']),
  		models.Index(fields=['tweet', 'parent']),
		models.Index(fields=['parent']),
		]
	
	def update_reaction_count(self):
		like_count = self.comment_likes.filter(reactiontype='like').count()
		unlike_count = self.comment_likes.filter(reactiontype='unlike').count()
		CommentModel.objects.filter(id=self.id).update(like_count=like_count,unlike_count=unlike_count)
		self.refresh_from_db()
	
	def update(self):
		self.refresh_from_db()
		return self

	def save(self,*args, **kwargs):
		super().save(*args, **kwargs)
		self.tweet. update_comment_count()
		if self.parent:
			reply_count=self.parent.replies.count()
			CommentModel.objects.filter(id=self.parent.id).update(reply_count=reply_count)
			self.parent.refresh_from_db()
  
	def delete(self, *args, **kwargs):
		parent=self.parent
		tweet=self.tweet
		super().delete(*args, **kwargs)
		tweet. update_comment_count()
		if parent:
			reply_count=parent.replies.count()
			CommentModel.objects.filter(id=parent.id).update(reply_count=reply_count)
			parent.refresh_from_db()
	
	def __str__(self):
		if self.parent:
			return f"{self.id}-------------{self.user.username} replied on {self.parent.id}"
		else:
			return f"{self.id}-------------{self.user.username} commented on {self.tweet.id}"

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, related_name='comment_likes')
    reactiontype= models.CharField(max_length=6)
    class Meta:
        unique_together = ['user', 'comment', 'reactiontype']
        indexes = [
            models.Index(fields=['user', 'reactiontype']),
            models.Index(fields=['comment', 'reactiontype']),
        ]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.comment.update_reaction_count()
    
    def delete(self, *args, **kwargs):
        comment = self.comment
        super().delete(*args, **kwargs)
        comment.update_reaction_count()
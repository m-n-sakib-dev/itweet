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
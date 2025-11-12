from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tweet(models.Model):
        user=models.ForeignKey(User,on_delete=models.CASCADE)
        text=models.TextField(max_length=280)
        photo=models.ImageField(upload_to='photos/',blank=True,null=True)
        created_at=models.DateTimeField(auto_now_add=True)
        updated_at=models.DateTimeField(auto_now=True)
        
        def __str__(self):
        	return f'{self.user.username} -- {self.text[:20]}'
 
class TweetModel(models.Model):
        user=models.ForeignKey(User,on_delete=models.CASCADE)
        text=models.TextField(max_length=1000,blank=True,null=True)
        photo=models.ImageField(upload_to='photos/',blank=True,null=True)
        like_count=models.IntegerField(default=0)
        unlike_count=models.IntegerField(default=0)
        comment_count=models.IntegerField(default=0)
        repost_count=models.IntegerField(default=0)
        created_at=models.DateTimeField(auto_now_add=True)
        updated_at=models.DateTimeField(auto_now=True)
        class Meta:
                ordering = ['-created_at']
        
        def update_reaction_count(self):
                self.like_count=self.reactionmodel_set.filter(reactiontype='like').count()
                self.unlike_count=self.reactionmodel_set.filter(reactiontype='unlike').count()
                self.save()
                
        def update_comment_count(self):
                self.comment_count = self.comments.count()
                self.save()
        
        
        def __str__(self):
        	return f'{self.user.username}--{self.user.username} -- {self.text[:20]}'
        
        
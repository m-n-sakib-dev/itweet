from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import RegexValidator
import re
# Create your models here.

class Tweet(models.Model):
        user=models.ForeignKey(User,on_delete=models.CASCADE)
        text=models.TextField(max_length=280)
        photo=models.ImageField(upload_to='photos/',blank=True,null=True)
        created_at=models.DateTimeField(auto_now_add=True)
        updated_at=models.DateTimeField(auto_now=True)
        
        def __str__(self):
        	return f'{self.user.username} -- {self.text[:20]}'
 
class Hashtag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tweet_count = models.IntegerField(default=0)
    is_trending = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-tweet_count', '-created_at']
        verbose_name = 'Hashtag'
        verbose_name_plural = 'Hashtags'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-tweet_count']),
        ]
    
    def __str__(self):
        return f'#{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('hashtag_detail', kwargs={'slug': self.slug})
    
    def increment_count(self):
        Hashtag.objects.filter(pk=self.pk).update(tweet_count=models.F('tweet_count') + 1)
        self.refresh_from_db()
    
    def decrement_count(self):
        Hashtag.objects.filter(pk=self.pk).update(tweet_count=models.F('tweet_count') - 1)
        self.refresh_from_db()
    
# Extract hashtags from text
    @classmethod
    def extract_hashtags(cls, text):
        return re.findall(r'#(\w+)', text)
    
    @classmethod
    def get_or_create_hashtags(cls, hashtag_names):
        hashtags = []
        for name in hashtag_names:
            name = name.lower().strip()
            if name:
                hashtag, created = cls.objects.get_or_create(
                    name=name,
                    defaults={'slug': slugify(name)}
                )
                hashtags.append(hashtag)
        return hashtags

 
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
        hashtags = models.ManyToManyField(Hashtag, related_name='tweets', blank=True)
        class Meta:
                ordering = ['-created_at']
        
        def update_reaction_count(self):
                TweetModel.objects.filter(pk=self.pk).update(
                        like_count=self.reactionmodel_set.filter(reactiontype='like').count(),
                        unlike_count=self.reactionmodel_set.filter(reactiontype='unlike').count()
                )
                self.refresh_from_db()

        def update_comment_count(self):
                TweetModel.objects.filter(pk=self.pk).update(
                        comment_count=self.comments.count()
                )
                self.refresh_from_db()
                
        def _process_hashtags(self):
                hashtag_names = Hashtag.extract_hashtags(self.text)
                hashtags = Hashtag.get_or_create_hashtags(hashtag_names)
                
                # Clear old hashtags and add new ones
                self.hashtags.clear()
                self.hashtags.add(*hashtags)
                
                # Increment count for each hashtag
                for hashtag in hashtags:
                        hashtag.increment_count()
        
        def save(self, *args, **kwargs):
                super().save(*args, **kwargs)
                self._process_hashtags()
                
                
        def delete(self, *args, **kwargs):
                # Decrement count before deletion
                for hashtag in self.hashtags.all():
                        hashtag.decrement_count()
                super().delete(*args, **kwargs)
                
        def __str__(self):
        	return f'{self.user.username}--{self.user.username} -- {self.text[:20]}'
        
        
class TrendingHashtag(models.Model):
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name='trending_entries')
    recent_tweets = models.IntegerField()  # Tweet count in last 24h
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recent_tweets']
    
    def __str__(self):
        return f"#{self.hashtag.name} ({self.recent_tweets})"
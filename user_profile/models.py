from django.db import models
from django.contrib.auth.models import User
from tweet.models import TweetModel
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    RELATIONSHIP_STATUS = [
        ('SINGLE', 'Single'),
        ('IN_RELATIONSHIP', 'In a relationship'),
        ('ENGAGED', 'Engaged'),
        ('MARRIED', 'Married'),
        ('COMPLICATED', "It's complicated"),
        ('SEPARATED', 'Separated'),
        ('DIVORCED', 'Divorced'),
        ('WIDOWED', 'Widowed'),
    ]
    
    # One-to-one link with Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    name=models.TextField(max_length=200,blank=True,null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Profile Images - SIMPLIFIED
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True,
        default='profile_pictures/default_avatar.jpg'
    )
    cover_photo = models.ImageField(
        upload_to='cover_photos/', 
        blank=True, 
        null=True,
        default='cover_photos/default_cover.jpg'
    )
    #follower Information
    follower_count=models.IntegerField(default=0)
    following_count=models.IntegerField(default=0)
    
    def update_follower_count(self):
        follower_count=self.user.follower.count()
        UserProfile.objects.filter(id=self.id).update(follower_count=follower_count)
        self.refresh_from_db()
        
        
    def update_following_count(self):
        following_count=self.user.following.count()
        UserProfile.objects.filter(id=self.id).update(following_count=following_count)
        self.refresh_from_db()
        
    
    # Location Information
    current_city = models.CharField(max_length=100, blank=True, null=True)
    hometown = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Professional Information
    workplace = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    education = models.CharField(max_length=200, blank=True, null=True)
    
    # Social Media Links
    website = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    # Relationship Information
    relationship_status = models.CharField(max_length=20, choices=RELATIONSHIP_STATUS, blank=True, null=True)
    
    # Privacy and Settings
    is_profile_public = models.BooleanField(default=True)
    show_email = models.BooleanField(default=False)
    show_phone = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def full_name(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        elif self.user.first_name:
            return self.user.first_name
        elif self.user.last_name:
            return self.user.last_name
        else:
            return self.user.username
        
    def primaryfields(self):
        return{
            'user_id':self.user.id,
            'name':self.name,
            'profile_picture':self.profile_picture.url,
            'cover_photo':self.cover_photo.url,
            'follower_count':self.follower_count,
            'following_count':self.following_count,
        }

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signal to automatically create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile=UserProfile.objects.create(user=instance)
        profile.name=profile.full_name
        profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    profile=instance.profile
    profile.name=profile.full_name
    profile.save()
    
    
class SavedTweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_tweet')
    tweet=models.ForeignKey(TweetModel,on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'tweet']  # Prevents duplicate saves
        ordering = ['-saved_at']  # Newest saves first

class FollowModel(models.Model):
    # the 'user' is following (who is doing the following)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    # the 'following_to' is whom is the user is follwoing (who is getting the follower)
    following_to= models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=['user','following_to']
        ordering=['-followed_at']
        indexes=[
            models.Index(fields=['user','following_to']),
            models.Index(fields=['following_to','user']),
        ]
        
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        print("updating counting on save")
        self.user.profile.update_following_count()
        self.following_to.profile.update_follower_count()
        
    def delete(self, *args, **kwargs):
        user_profile = self.user.profile
        target_profile = self.following_to.profile
        super().delete(*args, **kwargs)    
        print("updating counting")
        user_profile.update_following_count()
        target_profile.update_follower_count()
    
    def __str__(self):
        return f"{self.user.username} follows {self.following_to.username}"
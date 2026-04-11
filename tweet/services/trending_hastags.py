from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from ..models import Hashtag,TrendingHashtag  

def get_trending_hashtags(hours=24, limit=10):
    time_threshold = timezone.now() - timedelta(hours=hours)
    
    trending = Hashtag.objects.annotate(
        recent_tweets=Count('tweets', filter=Q(
            tweets__created_at__gte=time_threshold
        ))
    ).filter(
        recent_tweets__gt=0
    ).order_by('-recent_tweets', '-tweet_count')[:limit]
    
    return trending

def update_trending_table(request):
        trending_hashtags=get_trending_hashtags(hours=24,limit=10)
        TrendingHashtag.objects.all().delete()
        for t_hashtag in trending_hashtags:
                TrendingHashtag.objects.create(
			hashtag = t_hashtag,
			recent_tweets = t_hashtag.recent_tweets,
		)
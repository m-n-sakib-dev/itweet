import re
from django.utils.safestring import mark_safe
from ..services import update_trending_table
from ..models import TrendingHashtag
from django.http import JsonResponse
from django.forms.models import model_to_dict

#making hastag into clickable reference
def Hastagify(text):
        hashtag= re.sub(
        r'#(\w+)(\s*)',  # Group 1: word, Group 2: whitespace
        r'<span ><a href="" class="hashtag">#\1</a></span><span>\2</span>', 
        text
    )
        return mark_safe(hashtag)

def getTrendingHashtag(request):
        hashtags=TrendingHashtag.objects.all()
        trending_hashtags=[]
        for hashtag in hashtags:
                data = model_to_dict(hashtag)
                data['data']=model_to_dict(hashtag.hashtag)
                trending_hashtags.append(data)
        return JsonResponse({
		'success': True,
		'trending_hastags':trending_hashtags,
	})
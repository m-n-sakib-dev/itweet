import re
from django.utils.safestring import mark_safe
from ..services import update_trending_table
from ..models import TrendingHashtag, TweetModel, Hashtag
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render


tweet_per_page = 10


# making hastag into clickable reference
def Hastagify(text):
    hashtag = re.sub(
        r"#(\w+)(\s*)",  # Group 1: word, Group 2: whitespace
        r'<span ><a href="/hastags/\1/hashtag_page" class="hashtag">#\1</a></span><span>\2</span>',
        text,
    )
    return mark_safe(hashtag)


def getTrendingHashtag(request):
    hashtags = TrendingHashtag.objects.all()
    trending_hashtags = []
    for hashtag in hashtags:
        data = model_to_dict(hashtag)
        data["data"] = model_to_dict(hashtag.hashtag)
        trending_hashtags.append(data)
    return JsonResponse(
        {
            "success": True,
            "trending_hastags": trending_hashtags,
        }
    )


def HashtagTweetsPage(request, hashtag_name):
    user = request.user
    if user.is_authenticated:
        hashtag_name_lower = hashtag_name.lower()
        hashtag_tweets_count = Hashtag.objects.filter(name=hashtag_name_lower).count
        return render(
            request,
            "common_page.html",
            {
                "tweet_count": hashtag_tweets_count,
                "page": "Hashtag Tweets",
                "hashtag_name": hashtag_name,
            },
        )


def HashtagTweets(request, hashtag_name):
    from ..views import tweetAllData

    user = request.user
    page = int(request.GET.get("page", 1))
    start = tweet_per_page * (page - 1)
    end = tweet_per_page * page
    if request.user.is_authenticated:
        user = request.user
    else:
        return JsonResponse(
            {
                "success": False,
            }
        )
    hashtag_name_lower = hashtag_name.lower()
    tweets = TweetModel.objects.filter(
        hashtags__name=hashtag_name_lower
    ).select_related("user__profile")[start:end]
    tweets_data = tweetAllData(tweets, user)
    return JsonResponse(
        {
            "success": True,
            "tweets": tweets_data,
            "is_more": len(tweets_data) == tweet_per_page,
        }
    )

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from ..models import TweetModel,Hashtag
from user_profile.models import  UserProfile as UserProfileModel
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .hashtag import Hastagify
from user_profile.views.user_profile import BasicProfile

def Search(request):
        input=request.GET.get('input_str')
        input_type=request.GET.get('type')
        result=[]
        if(input_type=="hashtag"):
                matched_hastags=Hashtag.objects.filter(name__icontains=input)
                for hastag in matched_hastags:
                        result.append(model_to_dict(hastag))
        elif(input_type=='username'):
                matched_username=User.objects.filter(username__icontains=input)
                for user in matched_username:
                        result.append(BasicProfile(request,user.profile))
        else:
                print(input)
                matched_name=UserProfileModel.objects.filter(name__icontains=input)
                for profile in matched_name:
                        result.append(BasicProfile(request,profile))
        return JsonResponse({
		'success':True,
		'result':result,
	})
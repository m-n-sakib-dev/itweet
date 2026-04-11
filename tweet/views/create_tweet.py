from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from ..forms import TweetForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from ..models import TweetModel


@login_required
def CreateTweet(request):
   if request.method=='POST':
       form=TweetForm(request.POST,request.FILES)
       if form.is_valid():
           if 'photo' in request.FILES:
               photo=request.FILES['photo']
               name=photo.name.split('.')
               if len(name[0])>10: photo.name=name[0][0:10]+'.'+name[1]
               request.FILES['photo']=photo
           tweet=form.save(commit=False)
           tweet.user=request.user
           tweet.save()
           return redirect('tweet_feed')
   else:
       form=TweetForm()
   return render(request,'create_tweet.html',{'form':form})

@login_required
def TweetEdit(request,tweet_id):
    tweet=get_object_or_404(TweetModel,pk=tweet_id,user=request.user)
    if request.method=='POST':
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
           if 'photo' in request.FILES:
               photo=request.FILES['photo']
               name=photo.name.split('.')
               if len(name[0])>10: photo.name=name[0][0:10]+'.'+name[1]
               request.FILES['photo']=photo 
           tweet=form.save(commit=False)
           tweet.user=request.user
           tweet.save()
           return redirect('user_profile',user_id=request.user.id)
    else:
        form=TweetForm(instance=tweet)
    return render(request,'create_tweet.html',{'form':form})

@login_required
def shareTweet(request,tweet_id):
    if request.method=='POST':
        input_text=request.POST.get('input_text',None)
        parent_tweet=TweetModel.objects.get(id=tweet_id)
        if parent_tweet.parent != None:
            parent_tweet=parent_tweet.parent
        retweet=TweetModel.objects.create(user=request.user,parent=parent_tweet,text=input_text)
        print(retweet)
        return JsonResponse({
            'success':True
        })
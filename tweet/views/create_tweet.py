from django.contrib import messages
from django.shortcuts import render
from ..forms import TweetForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required


@login_required
def CreateTweet(request):
   if request.method=='POST':
       form=TweetForm(request.POST,request.FILES)
       if form.is_valid:
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
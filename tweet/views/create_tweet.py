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
           tweet=form.save(commit=False)
           tweet.user=request.user
           tweet.save()
           return redirect('tweet_list')
   else:
       form=TweetForm()
   return render(request,'tweet_form.html',{'form':form})
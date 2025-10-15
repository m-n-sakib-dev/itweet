from django.contrib import messages
from django.shortcuts import render
from ..models import Tweet
from ..forms import TweetForm,userRegistrationForm,userAuthenticationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
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

@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
           tweet=form.save(commit=False)
           tweet.user=request.user
           tweet.save()
           return redirect('tweet_list')
    else:
        form=TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})
@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    return 
    # if request.method=='POST':
    #     tweet.delete()
    #     return redirect('tweet_list')
    
    # return render(request,'tweet_confirm_delete.html',{'tweet':tweet})

def register(request):
    if request.method=='POST':
        form=userRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            messages.success(request, 'Registration successful! Welcome to TweetApp!')
            return redirect('tweet_list')
        else:
            messages.error(request,"could not register")
    else:
        form=userRegistrationForm()
    
    return render(request,'registration/registration.html',{'form':form})

def  userlogin(request):
    if request.method=='POST':
        form=userAuthenticationForm(request,request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request, f'Welcome back, {username}!')
                next_page = request.GET.get('next', 'tweet_list')
                return redirect(next_page)
            else:
                messages.error(request,'Invalid username of password')
    else:
        form=userAuthenticationForm()
    return render(request,'registration/login.html',{'form':form})
from ..forms import userRegistrationForm,userAuthenticationForm
from django.contrib.auth import login,authenticate
from django.shortcuts import redirect,render
from django.contrib import messages

def register(request):
    if request.method=='POST':
        form=userRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_feed')
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
                next_page = request.GET.get('next', 'tweet_feed')
                return redirect(next_page)
            else:
                messages.error(request,'Invalid username of password')
    else:
        form=userAuthenticationForm()
    return render(request,'registration/login.html',{'form':form})
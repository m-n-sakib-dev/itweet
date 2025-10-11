from django.contrib import messages
from django.shortcuts import render

from tweet.forms import TweetForm,userRegistrationForm,userAuthenticationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate


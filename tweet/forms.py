from django import forms
from .models import Tweet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class TweetForm(forms.ModelForm):
	class Meta:
		model=Tweet
		fields=['text','photo']
  
	def __init__(self,*args, **kwargs):
		super().__init__(*args,**kwargs)
		for field_name, field in self.fields.items():
			if isinstance(field.widget, forms.Textarea):
				field.widget.attrs['class'] = 'form-control'
				field.widget.attrs['rows'] = '3'
			elif isinstance(field.widget, forms.FileInput):
				field.widget.attrs['class'] = 'form-control'

class userRegistrationForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')
  
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for filed_name, filed in self.fields.items():
			filed.widget.attrs['class']='form-control'
   
class userAuthenticationForm(AuthenticationForm):
	class Meta:
		model=User
		fields=('username','password')
  
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for filed_name, filed in self.fields.items():
			filed.widget.attrs['class']='form-control'

	
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets={
                'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                'username': forms.TextInput(attrs={'class': 'form-control'}),
                 
                
        }
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            # Personal Information
            'bio', 'date_of_birth', 'gender', 'phone_number',
            
            # Profile Images
            'profile_picture', 'cover_photo',
            
            # Location Information
            'current_city', 'hometown', 'country',
            
            # Professional Information
            'workplace', 'position', 'education',
            
            # Social Media Links
            'website', 'facebook_url', 'twitter_url', 
            'instagram_url', 'linkedin_url',
            
            # Relationship Information
            'relationship_status',
            
            # Privacy Settings
            'is_profile_public', 'show_email', 'show_phone'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Tell people about yourself...'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'relationship_status': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'current_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current city'}),
            'hometown': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hometown'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'workplace': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where do you work?'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your position'}),
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your education'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourwebsite.com'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/username'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/username'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/username'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        # Make all fields not required
        for field in self.fields:
            self.fields[field].required = False
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ValidationError
import re


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }


class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            # Personal Information
            "bio",
            "date_of_birth",
            "gender",
            "phone_number",
            # Profile Images
            "profile_picture",
            "cover_photo",
            # Location Information
            "current_city",
            "hometown",
            "country",
            # Professional Information
            "workplace",
            "position",
            "education",
            # Social Media Links
            "website",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "linkedin_url",
            # Relationship Information
            "relationship_status",
            # Privacy Settings
            "is_profile_public",
            "show_email",
            "show_phone",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "bio": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Tell people about yourself...",
                }
            ),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "relationship_status": forms.Select(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+1234567890"}
            ),
            "current_city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Current city"}
            ),
            "hometown": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Hometown"}
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Country"}
            ),
            "workplace": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Where do you work?"}
            ),
            "position": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your position"}
            ),
            "education": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your education"}
            ),
            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://yourwebsite.com",
                }
            ),
            "facebook_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://facebook.com/username",
                }
            ),
            "twitter_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://twitter.com/username",
                }
            ),
            "instagram_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://instagram.com/username",
                }
            ),
            "linkedin_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://linkedin.com/in/username",
                }
            ),
            "profile_picture": forms.FileInput(attrs={"class": "form-control"}),
            "cover_photo": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        # Make all fields not required
        for field in self.fields:
            self.fields[field].required = False


class userRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="We'll send a verification email to this address.",
    )
    first_name = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                "maxlength": "10",
                "placeholder": "Max 10 chars",
                "pattern": ".{1,10}",
                "title": "Maximum 10 characters allowed",
            }
        ),
        help_text="Maximum 10 characters",
    )

    last_name = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                "maxlength": "10",
                "placeholder": "Max 10 chars",
                "pattern": ".{1,10}",
                "title": "Maximum 10 characters allowed",
            }
        ),
        help_text="Maximum 10 characters",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
        help_texts = {
            "username": "5-20 characters allowed. Letters, numbers, and ./+/-/_ characters can be used. Must start with  '@'.",
            "password1": "Password must contain at least 8 characters.",
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if username[0] != "@":
            raise ValidationError("Username Must Start with @")

        # Regex constraint: Only alphanumeric and specific special characters
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9.+-_]*$", username[1:]):
            raise ValidationError(
                "Username can only contain letters, numbers, and ./+/-/_ characters. Must start with  @"
            )

        # Length constraint
        if len(username) < 5 or len(username) > 20:
            raise ValidationError("Username must be at least 5 characters long.")

        # Reserved names constraint
        reserved_names = ["@admin", "@root", "@administrator", "@moderator", "@support"]
        if username.lower() in reserved_names:
            raise ValidationError(
                "This username is reserved. Please choose another one."
            )

        return username

    # Defining Emain constrains
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")

        # Email format validation using regex
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            raise ValidationError("Please enter a valid email address.")

        # Temporary email constraints
        temp_domains = ["tempmail.com", "10minutemail.com"]
        if any(domain in email for domain in temp_domains):
            raise ValidationError("Temporary email addresses are not allowed.")

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "").strip()
        if len(first_name) > 10:
            raise forms.ValidationError("First name cannot exceed 8 characters")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "").strip()
        if len(last_name) > 10:
            raise forms.ValidationError("Last name cannot exceed 8 characters")
        return last_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


class userAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed_name, filed in self.fields.items():
            filed.widget.attrs["class"] = "form-control"

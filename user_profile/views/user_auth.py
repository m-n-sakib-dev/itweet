from ..forms import userRegistrationForm, userAuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.contrib.auth.models import User
from django.conf import settings


def register(request):
    if request.method == "POST":
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            # user=form.save(commit=False)
            # user.set_password(form.cleaned_data['password1'])
            # user.save()
            # login(request,user)
            # return redirect('tweet_feed')
            request.session["registration_data"] = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password1"],
                "first_name": form.cleaned_data.get("first_name", ""),
                "last_name": form.cleaned_data.get("last_name", ""),
            }

            # 2. Verification code generate korbo
            verification_code = str(random.randint(100000, 999999))  # 6 digit code
            request.session["verification_code"] = verification_code

            # 3. Email e code pathabo
            send_mail(
                "Your iTweet Verification Code",
                f"""
Hello {form.cleaned_data["last_name"]},

Welcome to iTweet! Please verify your email address.

Your verification code is: {verification_code}

This code will expire in 10 minutes.

If you didn't create an account, please ignore this email.

Best regards,
iTweet Team
            """,
                settings.EMAIL_HOST_USER,
                [form.cleaned_data["email"]],
                fail_silently=False,
            )
            # 4. Verification page e redirect korbo
            return redirect("verify_email_page")
    else:
        form = userRegistrationForm()

    return render(request, "registration/registration.html", {"form": form})


# views.py
def verify_email_page(request):
    list(messages.get_messages(request))
    if "registration_data" not in request.session:
        # Session expired/already used
        messages.error(request, "Session expired. Please register again.")
        return redirect("registration")  # Back to registration

    if request.method == "POST":
        user_code = request.POST.get("verification_code", "").strip()
        saved_code = request.session.get("verification_code")

        if user_code == saved_code:
            # 1. Code match! Database e save korbo
            data = request.session.get("registration_data")

            # 2. User create korbo
            user = User(
                username=data["username"],
                email=data["email"],
                first_name=data["first_name"],
                last_name=data["last_name"],
            )
            user.set_password(data["password"])
            user.save()  # ✅ Ekhon database e save hobe

            # 3. Session clear korbo
            request.session.pop("registration_data", None)
            request.session.pop("verification_code", None)

            # 4. Auto login korbo
            login(request, user)

            # 5. Home page e redirect
            return redirect("tweet_feed")
        else:
            messages.error(request, "Invalid verification code")

    return render(request, "registration/verify_email.html")


# views.py
def resend_verification_code(request):
    list(messages.get_messages(request))
    # 1. Session theke email get korbo
    data = request.session.get("registration_data")
    if not data:
        return redirect("register")

    # 2. New code generate korbo
    new_code = str(random.randint(100000, 999999))
    request.session["verification_code"] = new_code

    # 3. Email pathabo
    send_mail(
        "Your New iTweet Verification Code",
        f"""
Hello {data["last_name"]},

Welcome to iTweet! Please verify your email address.

Your verification code is: {new_code}

This code will expire in 10 minutes.

If you didn't create an account, please ignore this email.

Best regards,
iTweet Team
            """,
        settings.EMAIL_HOST_USER,
        [data["email"]],
        fail_silently=False,
    )

    messages.success(request, "New code sent! Enter It above")
    return redirect("verify_email_page")


def userlogin(request):
    list(messages.get_messages(request))
    if request.method == "POST":
        form = userAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print("lhadsj")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                next_page = request.GET.get("next", "tweet_feed")
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = userAuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

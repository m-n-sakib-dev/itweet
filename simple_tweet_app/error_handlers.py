# simple_tweet_app/error_handlers.py
from django.shortcuts import render


def handler400(request, exception=None):
    context = {
        "exception": str(exception) if exception else None,
        "request_path": request.path,
    }
    return render(request, "400.html", context, status=400)


def handler403(request, exception=None):
    context = {
        "exception": str(exception) if exception else None,
        "request_path": request.path,
    }
    return render(request, "403.html", context, status=403)


def handler404(request, exception=None):
    context = {
        "exception": str(exception) if exception else None,
        "request_path": request.path,
    }
    return render(request, "404.html", context, status=404)


def handler500(request):
    return render(request, "500.html", status=500)

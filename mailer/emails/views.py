from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse

from mailer.emails.forms import EmailForm
from mailer.utils.helpers import Email, parse_to_html

# Create your views here.
def home(request):
    return render(request, "home.html", {})

def new_email(request):
    message = ""

    if request.method == "POST":
        form = EmailForm(request.POST)
        message = "Not so good"
        if form.is_valid():
            data = form.cleaned_data
            data["message"] = parse_to_html(data["message"])
            print(data["message"])
            email = Email(**data)
            result = email.send()
            print(result)
            messages.add_message(request, messages.INFO, str(result))
            return redirect(reverse('finish_email'))

    else:
        form = EmailForm()
    return render(request, "emails/new_emails.html", {"form": form})

def finish_email(request):
    return render(request, "emails/finish_email.html", {})
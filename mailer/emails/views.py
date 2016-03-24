from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse

from mailer import settings
from mailer.emails.forms import EmailForm
from mailer.emails.models import Email, Status, EmailStatus
from mailer.emails.dispachers import EmailDispacher
from mailer.utils.helpers import parse_to_html, get_object_or_None


def home(request):
    return render(request, "home.html", {})

def new_email(request):
    ''' Processing email sending requests and rendering the email send form'''

    email_id = request.GET.get("id", None)

    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email_object = form.save()

            data["message"] = parse_to_html(data["message"])
            data["carbon_copies"] = data["cc"]

            email = EmailDispacher(**data)
            results = email.send()

            for result in results:
                status = Status.objects.create(
                    provider=result.provider,
                    status=result.get_status(),
                    response=result.original_response
                    )
                EmailStatus.objects.create(email=email_object, status=status)
                messages.add_message(request, messages.INFO, str(result))

            return redirect(reverse('finish_email'))

    elif email_id:
        email = get_object_or_None(Email, id=email_id)
        form = EmailForm(initial={
            "sender": email.sender,
            "receivers": email.receivers,
            "cc": email.cc,
            "subject": email.subject,
            "message": email.message,
            })
    else:
        form = EmailForm()
    return render(request, "emails/new_emails.html", {"form": form})

def finish_email(request):
    return render(request, "emails/finish_email.html", {})

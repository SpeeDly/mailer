from django.shortcuts import render, redirect
from mailer.emails.forms import EmailForm 

# Create your views here.
def home(request):
    return render(request, "master.html", {})

def new_email(request):
    message = ""

    if request.method == "POST":
        form = EmailForm(request.POST)
        message = "Not so good"
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            message = "Bravo"
            # return redirect("new_email")
    else:
        form = EmailForm()
    return render(request, "emails/new_emails.html", {"form": form, "message": message})

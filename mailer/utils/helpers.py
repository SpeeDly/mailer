import mandrill
import sendgrid
import requests

from mailer import settings


MESSAGE = {
    'from_email': '',
    'from_name': '',
    'html': "",
    'important': False,
    'inline_css': None,
    'subject': "",
    'tags': [],
    'text': 'Example text content',
    'to': [{'email': 'recipient.email@example.com',
         'name': 'Recipient Name',
         'type': 'to'}],
}

# class SendGridEmailEngine:

#     def __init__(self, sender, receivers, subject, text, carbon_copies=None):
#         client = sendgrid.SendGridClient("SENDGRID_APIKEY")
#         message = sendgrid.Mail()

#         message.add_to("test@sendgrid.com")
#         message.set_from("you@youremail.com")
#         message.set_subject("Sending with SendGrid is Fun")
#         message.set_html("and easy to do anywhere, even with Python")

#         client.send(message)


#     def send(self):
#         result = self.mandrill_client.messages.send(message=self.message, async=False)
#         print(result)


class MandrillEmailEngine:

    def __init__(self, sender, receivers, subject, text, carbon_copies=None):
        self.mandrill_client = mandrill.Mandrill(settings.MANDRILL_APIKEY)
        self.message = MESSAGE
        self.message["from_email"] = sender
        self.message["html"] = text
        self.message["subject"] = subject
        self.message["to"] = subject

        to = []
        
        for receiver in receivers:
            to.append({
                "email": receiver,
                "type": "to"
                })

        if carbon_copies:
            for receiver in carbon_copies:
                to.append({
                    "email": receiver,
                    "type": "cc"
                    })

        self.message["to"] = to

    def send(self):
        result = self.mandrill_client.messages.send(message=self.message, async=False)
        print(result)


class MailGunEmailEngine:

    def __init__(self, sender, receivers, subject, text, carbon_copies=None):
        self.email = {
            "from": sender,
            "to": receivers,
            "subject": subject,
            "text": text
        }
        if carbon_copies:
            self.email["cc"] = carbon_copies

        print (",".join(receivers))

    def send(self):
        a = requests.post(
            "https://api.mailgun.net/v3/sandbox6ab8421b90e3479792deae38ac89fcb8.mailgun.org/messages",
            auth=("api", settings.MAILGUN_APIKEY),
            data=self.email)

        return a


class Email:

    def __init__(self, sender, receivers, subject, message, carbon_copy=None):
        __services = []
        self.sender = sender
        self.receivers = receivers
        self.carbon_copy = carbon_copy
        self.subject = subject
        self.message = message
        self.content_type = ""
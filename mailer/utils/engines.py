import mandrill
import requests

from mailer import settings
from mailer.utils.exceptions import MailerRequestsAPIError


MESSAGE = {
    'from_email': '',
    'from_name': '',
    'html': "",
    'important': False,
    'inline_css': None,
    'subject': "",
    'tags': [],
    'to': [{'email': 'recipient.email@example.com',
            'name': 'Recipient Name',
            'type': 'to'}],
}

MANDRILL_STATUSES = [
    "sent",
    "queued",
    "scheduled",
    "rejected",
    "invalid"
]

class ProviderResponse:

    def __init__(self, status, provider):
        self.status = status
        self.provider = provider

    def __str__(self):
        if self.status == "sent":
            return "Your email has been sent successfully with {}".format(self.provider)
        else:
            return "Something went wrong. Working on it!"


class MandrillEmailEngine:

    def __init__(self, *args, **kwargs):
        self.mandrill_client = mandrill.Mandrill(settings.MANDRILL_APIKEY)
        self.name = "Mandrill"
        self.message = MESSAGE
        self.message["from_email"] = kwargs.pop("sender", None)
        self.message["html"] = kwargs.pop("message", "None")
        self.message["subject"] = kwargs.pop("subject", None)

        self.message["to"] = []
        
        for receiver in kwargs.pop("receivers", []):
            self.message["to"].append({
                "email": receiver,
                "type": "to"
                })

        for receiver in kwargs.pop("carbon_copies", []):
            self.message["to"].append({
                "email": receiver,
                "type": "cc"
                })

    def parse_email_status(self, response):
        receivers_status = {}
        global_status = ""
        try:
            for item in response:
                email = item['email']
                status = item['status']
                if status == "sent":
                    global_status = "sent"

                if status not in MANDRILL_STATUSES:
                    status = 'unknown'

                receivers_status[email] = status
        except (KeyError, TypeError):
            raise MailerRequestsAPIError("Mandrill responsed in invalid format")

        return ProviderResponse(status, self.name)

    def get_api_call_data(self):
        return self.message

    def send(self):
        result = self.mandrill_client.messages.send(message=self.message, async=False)
        print(result)
        result = self.parse_email_status(result)
        return result


class MailGunEmailEngine:

    def __init__(self, *args, **kwargs):
        self.name = "Mailgun"
        self.email = {
            "from": kwargs.pop("sender", None),
            "to": kwargs.pop("receivers", []),
            "subject": kwargs.pop("subject", None),
            "html": kwargs.pop("message", None)
        }
        self.email["cc"] = kwargs.pop("carbon_copies", [])

    def parse_email_status(self, response):
        parsed_response = response.json()
        status = ""
        try:
            message_id = parsed_response["id"]
            message = parsed_response["message"]
            status = "sent"
        except (KeyError, TypeError):
            status = "invalid"
            raise MailerRequestsAPIError("Invalid Mailgun API response format", response=response)
        if not message == ("Queued. Thank you."):
            status = "invalid"
            raise MailerRequestsAPIError("Unrecognized Mailgun API message '{}'".format(message))

        return ProviderResponse(status, self.name)

    def get_api_call_data(self):
        return self.email

    def send(self):
        result = requests.post(
            settings.MAILGUN_SMPT,
            auth=("api", settings.MAILGUN_APIKEY),
            data=self.email)

        print(result)

        result = self.parse_email_status(result)

        return result

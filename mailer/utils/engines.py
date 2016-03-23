import mandrill
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

MANDRILL_STATUSES = [
    "sent",
    "queued",
    "scheduled",
    "rejected",
    "invalid"
]

class MandrillEmailEngine:

    def __init__(self, *args, **kwargs):
        self.mandrill_client = mandrill.Mandrill(settings.MANDRILL_APIKEY)
        self.message = MESSAGE
        self.message["from_email"] = kwargs.pop("sender", None)
        self.message["html"] = kwargs.pop("text", None)
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
        parsed_response = response.json()
        receivers_status = {}
        try:
            for item in parsed_response:
                email = item['email']
                status = item['status']
                if status not in MANDRILL_STATUSES:
                    status = 'unknown'
                receivers_status[email] = status
        except (KeyError, TypeError):
            pass
            # raise AnymailRequestsAPIError("Invalid Mandrill API response format")
        return receivers_status

    def get_api_call_data(self):
        return self.message

    def send(self):
        result = self.mandrill_client.messages.send(message=self.message, async=False)
        return result


class MailGunEmailEngine:

    def __init__(self, *args, **kwargs):
        self.email = {
            "from": kwargs.pop("sender", None),
            "to": kwargs.pop("receivers", []),
            "subject": kwargs.pop("subject", None),
            "text": kwargs.pop("text", None)
        }
        self.email["cc"] = kwargs.pop("carbon_copies", [])

    def parse_email_status(self, response):
        parsed_response = response.json()
        try:
            message_id = parsed_response["id"]
            mailgun_message = parsed_response["message"]
        except (KeyError, TypeError):
            pass
            # raise AnymailRequestsAPIError("Invalid Mailgun API response format",
            #                               email_message=message, payload=payload, response=response)
        if not mailgun_message == ("Queued. Thank you."):
            pass
            # raise AnymailRequestsAPIError("Unrecognized Mailgun API message '%s'" % mailgun_message,
            #                               email_message=message, payload=payload, response=response)

        return {"status": "sent"}

    def get_api_call_data(self):
        return self.email

    def send(self):
        result = requests.post(
            settings.MAILGUN_SMPT,
            auth=("api", settings.MAILGUN_APIKEY),
            data=self.email)

        result = self.parse_email_status(result)

        return result

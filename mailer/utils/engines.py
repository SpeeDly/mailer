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

    def send(self):
        result = requests.post(
            settings.MAILGUN_SMPT,
            auth=("api", settings.MAILGUN_APIKEY),
            data=self.email)

        return result

import mandrill
import requests

from mailer import settings


MANDRILL_MESSAGE_TEMPLATE = {
    'from_email': '',
    'from_name': '',
    'html': "",
    'important': False,
    'inline_css': None,
    'subject': "",
    'tags': [],
    'to2': [{
        'email': 'recipient.email@example.com',
        'name': 'Recipient Name',
        'type': 'to'
        }],
}

class ProviderResponse(object):
    ''' Basic implementation for a common data format between the engines
    '''
    def __init__(self, status, provider, receivers_status, original_response):
        self.status = status
        self.provider = provider
        self.receivers_status = receivers_status
        self.original_response = original_response

    def __str__(self):
        if self.is_successful():
            return "Your email has been sent successfully with {}".format(self.provider)
        else:
            return "{} failed to deliver your email.".format(self.provider)

    def get_status(self):
        '''Returning numeric representation of the status'''
        return settings.STATUSES.index(self.status)

    def is_successful(self):
        if self.status == settings.STATUSES[0]:
            return True
        return False


class EmailEngineInterface(object):
    ''' Base abstract class for email engines
        Based on the needs, it can be extended.
    '''
    def get_api_call_data(self):
        ''' Should return the original answer from the provider'''
        raise NotImplementedError(
            "Class %s doesn't implement get_api_call_data()" % (self.__class__.__name__))

    def send(self):
        ''' Should send email from the current provider
            Returns ProviderResponse object
        '''
        raise NotImplementedError(
            "Class %s doesn't implement send()" % (self.__class__.__name__))


class MandrillEmailEngine(EmailEngineInterface):
    ''' Mandrill email engine
    '''
    def __init__(self, **kwargs):
        self.mandrill_client = mandrill.Mandrill(settings.MANDRILL_APIKEY)
        self.name = "Mandrill"
        self.message = MANDRILL_MESSAGE_TEMPLATE
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
                if status == settings.STATUSES[0]:
                    global_status = settings.STATUSES[0]

                if status not in settings.STATUSES:
                    status = settings.STATUSES[6]

                receivers_status[email] = status
                if not global_status == settings.STATUSES[0]:
                    global_status = status

        except (KeyError, TypeError):
            global_status = settings.STATUSES[3]
        except:
            global_status = settings.STATUSES[4]

        if not global_status:
            global_status = settings.STATUSES[6]

        return ProviderResponse(global_status, self.name, receivers_status, response)

    def get_api_call_data(self):
        return self.message

    def send(self):
        result = self.mandrill_client.messages.send(message=self.message, async=False)
        result = self.parse_email_status(result)
        return result


class MailGunEmailEngine(EmailEngineInterface):

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
        status = ""
        message = ""
        try:
            message_id = response["id"]
            message = response["message"]
            status = settings.STATUSES[0]
        except (KeyError, TypeError):
            # Invalid Mailgun API response format"
            status = settings.STATUSES[4]

        if status == settings.STATUSES[0] and not message == ("Queued. Thank you."):
            # Unknown error
            status = settings.STATUSES[6]

        return ProviderResponse(status, self.name, None, response)

    def get_api_call_data(self):
        return self.email

    def send(self):
        response = requests.post(
            settings.MAILGUN_SMPT,
            auth=("api", settings.MAILGUN_APIKEY),
            data=self.email)

        result = self.parse_email_status(response.json())
        return result

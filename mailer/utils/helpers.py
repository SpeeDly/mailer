from django.utils.module_loading import import_string

from mailer import settings
from mailer.utils.exceptions import MailerRequestsAPIError


def get_connections():
    services = []
    for engine in settings.EMAIL_ENGINES:
        services.append(import_string(engine))
    return services


class Email:

    def __init__(self, **kwargs):
        self.__services = get_connections()
        self.email_data = {
            "sender": kwargs.pop("sender", None),
            "message": kwargs.pop("message", None),
            "subject": kwargs.pop("subject", None),
            "receivers": kwargs.pop("receivers", []),
            "carbon_copies": kwargs.pop("carbon_copies", [])
        }

    def add_email_service(self, service):
        self.__services.append(service)

    def get_registred_services(self):
        return [s for s in self.__services]

    def send(self):
        for service in self.__services:
            try:
                email = service(**self.email_data)
                result = email.send()
            except MailerRequestsAPIError as e:
                print(e.response)
        return result

def parse_to_html(message):
    tags_convertion = [
        ["[strong]", "<strong>"],
        ["[/strong]", "</strong>"],
        ["[i]", "<i>"],
        ["[/i]", "</i>"],
        ["[u]", "<u>"],
        ["[/u]", "</u>"],
        ["[font ", "<font "],
        ["[/font]", "</font>"],
    ]

    for rules in tags_convertion:
        message = message.replace(rules[0], rules[1])

    message = message.replace("']", "'>")


    return message
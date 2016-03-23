from django.utils.module_loading import import_string

from mailer import settings


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
            "text": kwargs.pop("text", None),
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
            except:
                print("err")

        return result
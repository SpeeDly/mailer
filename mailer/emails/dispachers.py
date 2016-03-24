from mailer.utils.helpers import get_connections


class EmailDispacher(object):
    ''' Email dispacher class, taking the imported engines in the
        settings file. It tryies to send email to the provider
        with higher priority, if it fails continue to the next one.
    '''
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
        ''' An option to manual add new mail engine '''
        self.__services.append(service)

    def get_registred_services(self):
        ''' Return a list with registred email engines '''
        return [s for s in self.__services]

    def send(self):
        ''' Trying to send email, starting with the first included service
            returns ProviderResponse object with seriliazed data from
            the requests. Finish on the first success.
        '''
        results = []
        for service in self.__services:
            email = service(**self.email_data)
            result = email.send()
            results.append(result)
            if result.is_successful():
                break

        return results

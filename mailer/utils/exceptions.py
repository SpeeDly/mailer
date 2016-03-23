import json

from django.core.exceptions import ImproperlyConfigured
from requests import HTTPError


class MailerError(Exception):

    def __init__(self, *args, **kwargs):
        """
        Optional kwargs:
          email_message: the original EmailMessage being sent
          status_code: HTTP status code of response to ESP send call
          response: requests.Response from the send call
        """
        self.email_message = kwargs.pop('email_message', None)
        self.status_code = kwargs.pop('status_code', None)
        if isinstance(self, HTTPError):
            # must leave response in kwargs for HTTPError
            self.response = kwargs.get('response', None)
        else:
            self.response = kwargs.pop('response', None)
        super(MailerError, self).__init__(*args, **kwargs)


class MailerAPIError(MailerError):
    """Exception for errors related with the API"""


class MailerRequestsAPIError(MailerAPIError, HTTPError):
    """Exception for unsuccessful response from a requests API."""

    def __init__(self, *args, **kwargs):
        super(MailerRequestsAPIError, self).__init__(*args, **kwargs)
        if self.response is not None:
            self.status_code = self.response.status_code


class MailerRecipientsRefused(MailerError):
    """Exception for send where all recipients are invalid or rejected."""

    def __init__(self, message=None, *args, **kwargs):
        if message is None:
            message = "All message recipients were rejected or invalid"
        super(MailerRecipientsRefused, self).__init__(message, *args, **kwargs)
from django.test import TestCase

from mailer.utils.engines import MailGunEmailEngine, MandrillEmailEngine
from mailer.utils.helpers import parse_to_html


class MailGunEmailEngineTests(TestCase):

    def test_initialization(self):
        data = {
            'sender': 'zhuhov@gmail.com',
            'subject': '',
            'receivers': ['zhuhov1@gmail.com', 'zhuhov2@gmail.com'],
            'carbon_copies': ['zhuhov4@gmail.com', 'zhuhov3@gmail.com'],
            'message': "message"
        }
        engine = MailGunEmailEngine(**data)
        request = engine.get_api_call_data()

        self.assertEqual(request["from"], 'zhuhov@gmail.com')
        self.assertEqual(request["to"], ['zhuhov1@gmail.com', 'zhuhov2@gmail.com'])
        self.assertEqual(request["subject"], "")
        self.assertEqual(request["html"], "message")

    def test_parse_email_status(self):
        data = {
            'sender': 'zhuhov@gmail.com',
            'subject': '',
            'receivers': ['zhuhov1@gmail.com', 'zhuhov2@gmail.com'],
            'carbon_copies': ['zhuhov4@gmail.com', 'zhuhov3@gmail.com'],
            'message': "message"
        }
        
        response = {'id': '<20160323224429.93123.83367.EBF2DAD8@sandbox6ab8421b90e3479792deae38ac89fcb8.mailgun.org>',
                    'message': 'Queued. Thank you.'}
        
        engine = MailGunEmailEngine(**data)
        parsed_status = engine.parse_email_status(response)

        self.assertEqual(parsed_status.is_successful(), True)
        self.assertEqual(parsed_status.provider, "Mailgun")
        self.assertEqual(parsed_status.original_response, response)

        response = {'id': '<20160323224429.93123.83367.EBF2DAD8@sandbox6ab8421b90e3479792deae38ac89fcb8.mailgun.org>'}
        
        engine = MailGunEmailEngine(**data)
        parsed_status = engine.parse_email_status(response)

        self.assertEqual(parsed_status.is_successful(), False)
        self.assertEqual(parsed_status.status, "invalid")
        self.assertEqual(parsed_status.provider, "Mailgun")
        self.assertEqual(parsed_status.original_response, response)

        response = {'id': '<20160323224429.93123.83367.EBF2DAD8@sandbox6ab8421b90e3479792deae38ac89fcb8.mailgun.org>',
                    'message': 'Wrong'}
        
        engine = MailGunEmailEngine(**data)
        parsed_status = engine.parse_email_status(response)

        self.assertEqual(parsed_status.is_successful(), False)
        self.assertEqual(parsed_status.status, "unknown")
        self.assertEqual(parsed_status.provider, "Mailgun")
        self.assertEqual(parsed_status.original_response, response)


class MandrillEmailEngineTests(TestCase):

    def test_initialization(self):
        data = {
            'sender': 'zhuhov@gmail.com',
            'subject': '',
            'receivers': ['zhuhov1@gmail.com', 'zhuhov2@gmail.com'],
            'carbon_copies': ['zhuhov4@gmail.com', 'zhuhov3@gmail.com'],
            'message': "message"
        }
        engine = MandrillEmailEngine(**data)
        request = engine.get_api_call_data()

        self.assertEqual(request["from_email"], 'zhuhov@gmail.com')
        self.assertEqual(request["to"], [
            {'email': 'zhuhov1@gmail.com', 'type': 'to'},
            {'email': 'zhuhov2@gmail.com', 'type': 'to'},
            {'email': 'zhuhov4@gmail.com', 'type': 'cc'},
            {'email': 'zhuhov3@gmail.com', 'type': 'cc'}
            ])

        self.assertEqual(request["subject"], "")
        self.assertEqual(request["html"], "message")

    def test_parse_email_status(self):
        data = {
            'sender': 'zhuhov@gmail.com',
            'subject': '',
            'receivers': ['zhuhov1@gmail.com', 'zhuhov2@gmail.com'],
            'carbon_copies': ['zhuhov4@gmail.com', 'zhuhov3@gmail.com'],
            'message': "message"
        }
        
        response = [{'email': 'zhuhov@gmail.com', '_id': 'd947604ca8114ab191c9279c202d7f47', 'reject_reason': None, 'status': 'sent'}]

        engine = MandrillEmailEngine(**data)
        parsed_status = engine.parse_email_status(response)

        self.assertEqual(parsed_status.is_successful(), True)
        self.assertEqual(parsed_status.provider, "Mandrill")
        self.assertEqual(parsed_status.original_response, response)

        response = [{'email': 'zhuhov@gmail.com', '_id': 'd947604ca8114ab191c9279c202d7f47', 'reject_reason': None, 'status': 'invalid'}]
        
        engine = MandrillEmailEngine(**data)
        parsed_status = engine.parse_email_status(response)

        self.assertEqual(parsed_status.is_successful(), False)
        self.assertEqual(parsed_status.status, "invalid")
        self.assertEqual(parsed_status.provider, "Mandrill")
        self.assertEqual(parsed_status.original_response, response)

        response = []
        
        engine = MandrillEmailEngine(**data)
        parsed_status = engine.parse_email_status(response)

        self.assertEqual(parsed_status.is_successful(), False)
        self.assertEqual(parsed_status.status, "unknown")
        self.assertEqual(parsed_status.provider, "Mandrill")
        self.assertEqual(parsed_status.original_response, response)


class parseToHtmlTests(TestCase):

    def test_parse_to_html(self):
        text = "[strong]fasf[/strong] [i]fwa[/i] [u]fwa[/u] [font color='blue']fwa[/font] wafaw"
        expected = "<strong>fasf</strong> <i>fwa</i> <u>fwa</u> <font color='blue'>fwa</font> wafaw"
        result = parse_to_html(text)
        self.assertEqual(result, expected)
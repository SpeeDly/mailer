from django.test import TestCase

from mailer.emails.forms import EmailForm


class EmailFormTests(TestCase):

    def test_form_validation(self):
        form_data = {
            'sender': 'zhuhov@gmail.com',
            'subject': '',
            'receivers': 'zhuhov1@gmail.com, zhuhov2@gmail.com',
            'cc': 'zhuhov4@gmail.com, zhuhov3@gmail.com',
            'message': "message"
            }
        form = EmailForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = {
            'sender': 'zhuhov@gmail.com',
            'subject': '',
            'receivers': '',
            'cc': 'zhuhov4@gmail.com, zhuhov3@gmail.com',
            'message': "message"
            }

        form = EmailForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'sender': 'zhuhov@gmail.com',
            'subject': '',
            'receivers': 'zhuhov1@gmail.com',
            'cc': 'zhuhov4@gmail.com, zhuhov3@gmail',
            'message': "message"
            }

        form = EmailForm(data=form_data)
        self.assertFalse(form.is_valid())
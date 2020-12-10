from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()



from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def do_send_email(
				pEmailTemplate, 
				pSubject, 
				pTo, 
				emHdrTitle, 
                emSubHdrTitle, 
                emName, 
                messageFirst,
                messageSecond,
                call2ActionText,
                call2ActionLink,
                userEmail
                ):
    """
    The common function to auto send email to the user when triggered.
    """
    msg_html = render_to_string('emails/'+pEmailTemplate,
                                {
                                	'EMAIL_HEADER_TITLE': emHdrTitle,
                                    'EMAIL_SUB_TITLE': emSubHdrTitle,
                                    'USERNAME': emName,
                                    'USER_EMAIL': userEmail,
                                    'SUBJECT': pSubject,
                                    'MESSAGE_FIRST': messageFirst,
                                    'MESSAGE_SECOND': messageSecond,
                                    'CALL_2_ACTION_TEXT': call2ActionText,
                                    'CALL_2_ACTION_LINK': call2ActionLink,
                                    # variables from settings
                                    'SITE_SHORT_NAME': settings.SITE_SHORT_NAME,
                                    'SITE_FULL_NAME': settings.SITE_FULL_NAME,
                                    'BASE_URL': settings.BASE_URL,
                                    'COMPANY_ADDRESS': settings.COMPANY_ADDRESS,
                                    'UNSUBSCRIBE_MESSAGE': settings.UNSUBSCRIBE_MESSAGE,
                                    'UNSUBSCRIBE_LINK': settings.UNSUBSCRIBE_LINK,
                                 }
                                 )
    msg = EmailMessage(
					subject=pSubject, 
    				body=msg_html,
                   from_email=settings.EMAIL_HOST_USER, 
                   to=pTo, 
                   cc=None,
                   bcc=["'"+settings.APP_EMAIL_BCC+"'"]
                       )
    msg.content_subtype = "html"
    msg.send()
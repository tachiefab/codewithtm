
from celery.decorators import task
from django.core.mail import EmailMessage
from .utils import do_send_email


@task(name="send_email")
def send_email(data):

    username = data['username']
    preview_header = data['preview_header']
    subject = data['subject']
    message_first = data['message_first']
    message_second = data['message_second']
    call2action_text = data['call2action_text']
    call2action_link = data['call2action_link']
    email_lists = [data['to_email']]

    do_send_email(
                  'email.html',
                  subject,
                  email_lists,
                  subject,
                  preview_header,
                  username,
                  message_first,
                  message_second,
                  call2action_text,
                  call2action_link,
                  None
              )



@task(name="contact_us_send_email")
def contact_us_send_email(data):

    full_name = data['full_name']
    preview_header = data['preview_header']
    subject = data['subject']
    message = data['message']
    user_email = data['user_email']
    email_lists = [data['to_email']]

    do_send_email(
                  'contact_us.html',
                  subject,
                  email_lists,
                  subject,
                  preview_header,
                  full_name,
                  message,
                  None,
                  None,
                  None,
                  user_email
              )
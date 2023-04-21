from django.core.mail import send_mail
from django.template.loader import render_to_string

from api_yamdb.settings import EMAIL_HOST_USER


def send_message(email, template, context):
    """
    Отправка сообщений по электронной почте.
    Принимает email, словарь контекста с данными,
    f-строку(или просто строку) с путем до шаблона
    сообщения.
    """
    message = render_to_string(template, context)

    send_mail(
        'Код подтверждения',
        message,
        EMAIL_HOST_USER,
        [email],
        html_message=message
    )

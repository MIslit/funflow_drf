from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from celery import shared_task

@shared_task
def send_email():  
    with get_connection(  
        host=settings.EMAIL_HOST, 
     port=settings.EMAIL_PORT,  
     username=settings.EMAIL_HOST_USER, 
     password=settings.EMAIL_HOST_PASSWORD, 
     use_tls=settings.EMAIL_USE_TLS  
       ) as connection:  
           subject = 'Успешный успех!' 
           email_from = settings.EMAIL_HOST_USER  
           recipient_list = ['imaks1464@gmail.com', ]  
           message = 'Вы успешно добавили идею' 
           EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
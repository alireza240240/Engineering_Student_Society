from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def notify_admin_new_article(article_title, author_username):
    subject = "New Article Submitted"
    message = f"A new article titled '{article_title}' has been submitted by {author_username}. Please check for approve or reject."
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ["example@gmail.com"],  # enter admin email
        fail_silently=False,
    )


from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from .models import PostCategory
from django.db.models.signals import m2m_changed
import datetime
from django.utils import timezone
from datetime import timedelta
from news.models import Post, Category
from django.conf import settings


@shared_task
def send_notify_add_news(preview, pk, title, subscribers):
    html_content = render_to_string(
        'sub_post_created_email.html',
        {
            'text': preview,
            'link': f' http://127.0.0.1:8000/posts/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for postCategory in categories:
            subscribers += postCategory.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notify_add_news(instance.preview(), instance.pk, instance.title, subscribers)


@shared_task
def send_notif_week():
    today = datetime.datetime.now(tz=timezone.utc)
    week = timedelta(days=7)
    last_week = today - week
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': 'http://127.0.0.1/posts/',
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

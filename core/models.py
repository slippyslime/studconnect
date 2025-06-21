from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    STUDENT = "student"
    TEACHER = "teacher"
    DEAN = "dean"
    ROLE_CHOICES = [
        (STUDENT, "Студент"),
        (TEACHER, "Преподаватель"),
        (DEAN, "Деканат"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Message(models.Model):
    sender      = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name="sent_messages")
    recipients  = models.ManyToManyField(User, related_name="received_messages")
    subject     = models.CharField(max_length=200, blank=True)
    body        = models.TextField()
    created_at  = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.subject or self.body[:40]}…"


class MessageStatus(models.Model):
    SENT    = "sent"
    READ    = "read"
    REPLIED = "replied"
    STATUS_CHOICES = [
        (SENT,    "Отправлено"),
        (READ,    "Прочитано"),
        (REPLIED, "Отвечено"),
    ]

    message     = models.ForeignKey(Message, on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    status      = models.CharField(max_length=8, choices=STATUS_CHOICES,
                                   default=SENT)
    changed_at  = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("message", "user")   # один статус на пару

    def __str__(self):
        return f"{self.user}: {self.get_status_display()} @ {self.changed_at:%d.%m %H:%M}"

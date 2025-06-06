from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    TextField,
)

from config.settings import AUTH_USER_MODEL


class Recipient(models.Model):
    email = CharField(max_length=100, unique=True)
    fullname = CharField(max_length=100)
    comment = TextField(verbose_name="комментарий")
    owner = ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="Создатель клиента",
        help_text="Укажите создателя клиента",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["email", "fullname"]


class Message(models.Model):
    subject_letter = CharField(max_length=100, unique=True, verbose_name="тема")
    body_letter = TextField(verbose_name="комментарий")
    owner = ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="Владелец рассылки",
        help_text="Укажите владельца рассылки",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["subject_letter", "body_letter"]

    def __str__(self):
        return self.subject_letter


class Mailing(models.Model):
    CREATED = "created"
    STARTED = "started"
    ENDED = "ended"

    STATUS_IN_CHOICES = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (ENDED, "Завершена"),
    ]

    first_sending = DateTimeField(
        verbose_name="Время начала", auto_now_add=True, editable=False
    )
    last_sending = DateTimeField(
        verbose_name="Время конца", auto_now_add=True, editable=False
    )
    status = CharField(
        choices=STATUS_IN_CHOICES,
        max_length=10,
        verbose_name="Статус",
        default=CREATED,
        editable=False,
    )
    message = ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    recipient = ManyToManyField(
        Recipient, related_name="mailings", verbose_name="Клиент"
    )
    owner = ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="Владелец рассылки",
        help_text="Укажите владельца рассылки",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    is_active = BooleanField(default=True, blank=True, null=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["first_sending", "last_sending", "status"]
        permissions = [("can_disabling_mailings", "can disabling mailings")]


class AttemptMailing(models.Model):
    SUCCESS = "success"
    NOT_SUCCESS = "not success"

    STATUS_IN_CHOICES = [
        (SUCCESS, "Успешно"),
        (NOT_SUCCESS, "Не успешно"),
    ]

    date_attempt = DateTimeField(
        verbose_name="Дата и время попытки", auto_now_add=True, editable=False
    )
    status = CharField(
        choices=STATUS_IN_CHOICES, max_length=11, verbose_name="Статус", editable=False
    )
    answer = TextField(verbose_name="Ответ почтового сервера", editable=False)
    mailing = ForeignKey(
        Mailing,
        related_name="attempts",
        verbose_name="Попытка",
        on_delete=models.CASCADE,
    )
    owner = ForeignKey(
        AUTH_USER_MODEL,
        verbose_name="Владелец попытки рассылки",
        help_text="Укажите владельца попытки рассылки",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["date_attempt", "status", "answer", "mailing"]


owner = models.ForeignKey(
    get_user_model(),
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    verbose_name="Владелец",
)

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    """Модель подписки на авторов"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Пользователь',
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор',
                               )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(
                    user=models.F('author')
                ), name='user=author'),
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='users follow on uniq authors'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
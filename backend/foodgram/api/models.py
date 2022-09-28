from django.contrib.auth import get_user_model
from django.db import models
from recipes.models import Receipe

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


class Favorite(models.Model):
    """Модель избранных рецептов"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь',
                             )
    receipe = models.ForeignKey(
        Receipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorite_receip',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'receipe'], name='uniq receips in favorites'
            )
        ]


class ShoppingChart(models.Model):
    """Модель списка покупок"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_chart',
        verbose_name='Пользователь',
    )
    receipe = models.ForeignKey(
        Receipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_chart_receip',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shopping_chart'
            )
        ]

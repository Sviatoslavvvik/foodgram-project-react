from django.contrib.auth import get_user_model
from django.db import models
from recipes.models import Receipe

User = get_user_model()


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
                fields=['user', 'receipe'], name='unique_shopping_chart'
            )
        ]

from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель тэга"""
    name = models.CharField(
        'Название тега',
        db_index=True,
        unique=True,
        max_length=200,
    )
    color = models.CharField(
        'Цветовой HEX-код',
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                           message='Цвет не в формате Hex')
        ]
    )
    slug = models.SlugField(
        'Slug',
        unique=True,
        max_length=200,
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента"""
    name = models.CharField(
        'Название',
        db_index=True,
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return self.name


class Receipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации (пользователь)'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
        max_length=2000,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        through='IngredientInRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тэгов',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[MinValueValidator(1), MaxValueValidator(60*5)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """Количество ингридиента в рецепте"""
    receipe = models.ForeignKey(
        Receipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amounts',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        max_digits=4, decimal_places=1,
        verbose_name='Количество',
        validators=[MinValueValidator(0.1), MaxValueValidator(4999.99)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'receipe'),
                name='unique_recipe_ingredient'
            )
        ]
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецепте'

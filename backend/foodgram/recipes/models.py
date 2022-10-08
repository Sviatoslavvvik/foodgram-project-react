from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель тэга"""
    name = models.CharField(
        verbose_name='Название тега',
        db_index=True,
        unique=True,
        max_length=200,
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        unique=True,
        max_length=200,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Ingridient(models.Model):
    """Модель ингридиента"""
    name = models.CharField(
        verbose_name='Название',
        db_index=True,
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            )
        ]


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
    )
    ingredients = models.ManyToManyField(
        Ingridient,
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
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )


class IngredientInRecipe(models.Model):
    """Количество ингридиента в рецепте"""
    receipe = models.ForeignKey(
        Receipe,
        on_delete=models.CASCADE,
        related_name='ingridients_amounts',
    )
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('ingridient', 'receipe'),
                name='unique_recipe_ingredient'
            )
        ]
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецепте'

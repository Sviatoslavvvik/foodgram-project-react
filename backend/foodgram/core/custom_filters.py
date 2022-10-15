from django_filters import (AllValuesMultipleFilter, BaseInFilter, CharFilter,
                            FilterSet, NumberFilter)

from recipes.models import Ingredient, Receipe  # isort:skip


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class RecipeFilter(FilterSet):
    """Фильтрация рецептов"""
    tags = AllValuesMultipleFilter(field_name='tags__slug', conjoined=False,)
    is_favorited = NumberInFilter(
        field_name='is_favorited', method='filter_receipe', lookup_expr='in',
    )
    is_in_shopping_cart = NumberInFilter(
        field_name='is_in_shopping_cart', method='filter_receipe',
        lookup_expr='in',
    )

    def filter_receipe(self, queryset, name, value):
        if self.request.query_params.get("is_favorited"):
            queryset = queryset.filter(favorite_receip__user=self.request.user)
        if self.request.query_params.get("is_in_shopping_cart"):
            queryset = queryset.filter(
                shopping_chart_receip__user=self.request.user
            )
        return queryset

    class Meta:
        model = Receipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')


class IngredientFilter(FilterSet):
    """Поиск ингредиентов по имени"""
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)

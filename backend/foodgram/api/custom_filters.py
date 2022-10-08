from django_filters import (AllValuesMultipleFilter, BooleanFilter, CharFilter,
                            FilterSet)
from recipes.models import Ingridient, Receipe


class RecipeFilter(FilterSet):
    """Фильтрация рецептов"""
    tags = AllValuesMultipleFilter(field_name='tags', conjoined=False,)
    is_favorited = BooleanFilter(
        field_name='is_favorited', method='filter_receipe'
    )
    is_in_shopping_cart = BooleanFilter(
        field_name='is_in_shopping_cart', method='filter_receipe'
    )

    def filter_receipe(self, queryset, name, value):
        if self.request.query_params.get("is_favorited"):
            queryset = queryset.filter(favorites__user=self.request.user)
        if self.request.query_params.get("is_in_shopping_cart"):
            queryset = queryset.filter(
                shopping_chart_receip_user=self.request.user
            )
        return queryset

    class Meta:
        model = Receipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')


class IngredientFilter(FilterSet):
    """Поиск ингредиентов по имени"""
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingridient
        fields = ("name",)

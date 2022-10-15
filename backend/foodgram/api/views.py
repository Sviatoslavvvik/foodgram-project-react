from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.custom_filters import IngredientFilter, RecipeFilter  # isort:skip
from core.custom_paginator import CustomPagination  # isort:skip
from core.custom_permission import (AuthorChangePermission,  # isort:skip
                                    UserDeletePermission)  # isort:skip
from .models import Favorite, ShoppingChart  # isort:skip
from .serializers import (IngredientSerializer,  # isort:skip
                          ReceipeSerializer,
                          RecipeWriteSerializer,  # isort:skip
                          TagSerializer)  # isort:skip
from users.serializers import RecipeShortDataSerializer  # isort:skip
from recipes.models import (Ingredient,  # isort:skip
                            IngredientInRecipe, Receipe, Tag)  # isort:skip

User = get_user_model()


class IngridientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_class = IngredientFilter
    search_fields = ("^name",)
    ordering_fields = ("^name",)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class ReceipeViewSet(viewsets.ModelViewSet):
    queryset = Receipe.objects.all()
    serializer_class = ReceipeSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('favorite', 'shopping_cart'):
            return RecipeShortDataSerializer
        if self.request.method in ('POST', 'PUT', 'PATCH'):
            return RecipeWriteSerializer
        return ReceipeSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE' and (
            self.action == 'favorite' or self.action == 'shopping_cart'
        ):
            return (UserDeletePermission(),)
        if self.request.method in ('PATCH', 'DELETE'):
            return (AuthorChangePermission(),)
        return super().get_permissions()

    @action(
        detail=True,
        methods=("POST", "DELETE"),
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk=None):
        user = request.user
        obj = self.get_object()
        favorite = Favorite.objects.filter(user=user, receipe=obj).exists()
        if request.method == "POST" and not favorite:
            Favorite.objects.create(user=user, receipe=obj)
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE" and favorite:
            Favorite.objects.filter(user=user, receipe=obj).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Ошибка удаления из избранного"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True,
        methods=("POST", "DELETE"),
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        obj = self.get_object()
        in_cart = ShoppingChart.objects.filter(user=user, receipe=obj).exists()
        if request.method == "POST" and not in_cart:
            ShoppingChart.objects.create(user=user, receipe=obj)
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE" and in_cart:
            ShoppingChart.objects.filter(user=user, receipe=obj).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Ошибка удаления из списка покупок"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=False,
        methods=("GET",),
        permission_classes=(IsAuthenticated, )
    )
    def download_shopping_cart(self, request):
        user = request.user
        in_cart = IngredientInRecipe.objects.filter(
            receipe__shopping_chart_receip__user=user
        )
        queryset = in_cart.values_list(
            "ingredient__name",
            "ingredient__measurement_unit"
        ).annotate(
            amount_sum=Sum(
                "amount"
            )
        )
        text = ''
        for ingredient in queryset:
            text += (
                f"{list(ingredient)[0]} - "
                f"{list(ingredient)[2]} "
                f"{list(ingredient)[1]} \n"
            )
        response = HttpResponse(text, content_type='application/txt')
        response[
            "Content-Disposition"] = 'attachment; filename="MyPurchases.txt"'
        return response

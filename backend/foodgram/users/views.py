from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.custom_paginator import CustomPagination  # isort:skip
from core.custom_viewset import CreateListRetrieveViewSet  # isort:skip
# from core.custom_filters import ReceipSubscriptionsFilter  # isort:skip
from .models import Subscription  # isort:skip
from .serializers import (MakeSubscribeSerializer,  # isort:skip
                          SetPasswordSerializer,
                          SignUpSerializer, SubscriptionsUserSerializer,
                          UserProfileSerializer)  # isort:skip


User = get_user_model()


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all().order_by('email')
    serializer_class = UserProfileSerializer
    pagination_class = CustomPagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action == 'create':
            return SignUpSerializer
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action == 'subscriptions':
            return SubscriptionsUserSerializer
        if self.action == 'subscribe':
            return MakeSubscribeSerializer

        return UserProfileSerializer

    @action(
        detail=False,
        methods=('GET',),
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=('POST',),
        permission_classes=(IsAuthenticated, )
    )
    def set_password(self, request):
        serializer = self.get_serializer(data=self.request.data,
                                         instance=self.request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=("POST", "DELETE"),
        permission_classes=(IsAuthenticated, ),
    )
    def subscribe(self, request, pk=None):
        user = request.user
        obj = self.get_object()
        is_subscribed = Subscription.objects.filter(
            user=user, author=obj
        ).exists()
        if request.method == "POST" and not is_subscribed:
            Subscription.objects.create(user=user, author=obj)
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == "DELETE" and is_subscribed:
            Subscription.objects.filter(user=user, author=obj).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Действие запрещено"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=False,
        methods=("GET",),
        permission_classes=(IsAuthenticated,),
        pagination_class=CustomPagination,
    )
    def subscriptions(self, request):
        user = request.user
        new_queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(new_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionsUserSerializer(
            new_queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)

from api.custom_viewset import CreateListRetrieveViewSet
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (SetPasswordSerializer, SignUpSerializer,
                          UserProfileSerializer)

User = get_user_model()


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return SignUpSerializer
        if self.action == 'set_password':
            return SetPasswordSerializer
        return UserProfileSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['current_password'] = self.request.data.get('current_password')
        return context

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(IsAuthenticated, )
     )
    def set_password(self, request):
        serializer = self.get_serializer(data=self.request.data,
                                         instance=self.request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

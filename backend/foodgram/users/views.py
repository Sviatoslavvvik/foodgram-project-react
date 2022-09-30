from api.custom_viewset import CreateListRetrieveViewSet
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import SignUpSerializer, UserProfileSerializer

User = get_user_model()


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return SignUpSerializer
        return UserProfileSerializer 

    @action(
        detail=False,
        methods=['get'],
        # permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(
    #     detail=False,
    #     methods=['get'],
    #  )
    # def set_password(self, request):

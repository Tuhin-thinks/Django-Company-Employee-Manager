from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from companyusers.models import Company

from .serializers.user_serializer import UserDetailSerializer, UserSerializer

UserModel = get_user_model()


class UserListAPIView(generics.ListAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "email"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print("Inside get_queryset")
        queryset = UserModel.objects.all()
        return queryset


class UserDetailAPIView(ModelViewSet):
    serializer_class = UserSerializer
    lookup_field = ()
    lookup_url_kwarg = False

    serializer_class = UserDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

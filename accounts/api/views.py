from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView,RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework import views
from accounts.models import User
from .serializers import UserRegistrationSerializer, LoginSerializer, UserSerializer


# Create your views here.

class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []

    # permission_classes = [permissions.AllowAny]
    # We need to work on the request on serializers.py so we send request context to serializers with this method

    def get_serializer_context(self):
        return {'request': self.request}


class LoginAPIView(views.APIView):
    permission_classes = [AllowAny]
    # permission_classes = []
    # renderer_classes = JSONRenderer
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = []
    # permission_classes = []
    # renderer_classes = (UserJSONRenderer)
    serializer_class = UserSerializer
    # queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSON field and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # def update(self, request, *args, **kwargs):
    #     # serializer_data = request.data.get('user', {})
    #     serializer_data = request.data
    #
    #     # Here is that serialize, validate, save pattern we talked about
    #     # before.
    #     serializer = self.serializer_class(
    #         request.user, data=serializer_data, partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = []
    # permission_classes = []
    # renderer_classes = (UserJSONRenderer)
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        # serializer_data = request.data.get('user', {})
        serializer_data = request.data

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "User Updated Successfully"}, status=status.HTTP_200_OK)

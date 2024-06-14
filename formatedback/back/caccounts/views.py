from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer, CustomUserSerializer
import logging

logger = logging.getLogger(__name__)


class RegistrationAPIView(APIView):
    """
    Registers a new user.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {'token': serializer.data.get('token')},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.exception("An error occurred during user registration:")
            return Response({'error': 'An error occurred during user registration.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            print("User authenticated successfully:", user)
            return Response({'token': user.token, 'userName': user.name}, status=status.HTTP_200_OK)
        except ValidationError as e:
            print('Validation Error:', e.detail)
            print('Request Data:', request.data)
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("An error occurred during login:", exc_info=True)
            return Response({'error': 'An error occurred during login.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserInfoAPIView(APIView):
    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

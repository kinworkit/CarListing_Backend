import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import CustomUser
from django.contrib.auth import authenticate


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None, None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token.')

        user = None

        if 'email' in payload:
            user = self._authenticate_email(payload['email'], payload.get('password'))
        elif 'phone' in payload:
            try:
                user = CustomUser.objects.get(phone=payload['phone'])
            except CustomUser.DoesNotExist:
                raise exceptions.AuthenticationFailed('No user matching this phone was found.')
        else:
            raise exceptions.AuthenticationFailed('Invalid token format.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('This user has been deactivated.')

        return (user, token)

    def _authenticate_email(self, email, password):
        if not email or not password:
            raise exceptions.AuthenticationFailed('Email and password are required for email authentication.')

        user = authenticate(request=None, email=email, password=password)

        if user is None:
            raise exceptions.AuthenticationFailed('No user matching this email was found.')

        return user

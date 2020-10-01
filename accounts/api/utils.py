import datetime
from django.utils import timezone
from django.conf import settings

expire_detla = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']


# Function overidden for custom exipration time of token
def jwt_response_payload_handler(token, user):
    return {
        'token': token,
        'user': user.username,
        # Manual expiration time
        # Substration is for response delay
        'expires': timezone.now() + expire_detla - datetime.timedelta(seconds=200)
    }

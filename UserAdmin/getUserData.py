import jwt
from django.conf import settings
from django.contrib.auth.models import User
from .models import UserProfile
from AccountAdmin.models import AccountProfile
from rest_framework.exceptions import AuthenticationFailed


def get_user_from_token(token):
    try:
        # Decode the token using your secret key
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])

        # Extract user ID from the payload
        user_id = payload.get('user_id')  # Ensure this matches your token structure

        # Fetch the user and associated user profile
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
        account_details = (AccountProfile.objects.get(user=user))

        # Prepare the user data to return
        user_data = {
            'username': user.username,
            'email': user.email,
            'phone_number': user_profile.phone_number,
            'profile_picture_url': user_profile.profile_picture_url,
            'date_of_birth': user_profile.date_of_birth,
            'created_at': user_profile.created_at,
            'updated_at': user_profile.updated_at,
            'public_address': account_details.public_address,
        }

        return user_data

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.DecodeError:
        raise AuthenticationFailed('Invalid token')
    except User.DoesNotExist:
        raise AuthenticationFailed('User not found')
    except UserProfile.DoesNotExist:
        raise AuthenticationFailed('User profile not found')

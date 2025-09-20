# STEP 1: Create accounts/authentication.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Look for user by EMAIL instead of username
            user = User.objects.get(email=username)  # username parameter contains email
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
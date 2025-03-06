from django.contrib.auth.backends import ModelBackend
from app.models import CustomUser  # ✅ Import your custom user model

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=username)  # ✅ Authenticate using email
            if user.check_password(password):  # ✅ Verify password
                return user
        except CustomUser.DoesNotExist:
            return None
        return None

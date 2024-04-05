from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_id"] = user.id
        token["username"] = user.username
        # Assuming UserProfile is related through 'user' field
        if hasattr(user, 'userprofile'):
            token["onboarding"] = user.userprofile.onboarding
        else:
            token["onboarding"] = True  # Set default value if UserProfile doesn't exist
        return token


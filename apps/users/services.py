from apps.common.base import BaseService
from .models import User


class UserService(BaseService):

    model = User

    @staticmethod
    def create_user_or_superuser(validated_data):
        if validated_data.get("is_superuser", False):
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)
        
        return user
    
    @staticmethod
    def update_user(user, validated_data):
        if "email" in validated_data:
            validated_data["email"] = validated_data.get("email").lower()

        if "first_name" in validated_data:
            validated_data["first_name"] = validated_data.get("first_name").title()

        if "last_name" in validated_data:
            validated_data["last_name"] = validated_data.get("last_name").title()

        password = validated_data.pop("password", None)

        if password is not None:
            user.set_password(password)

        user.save()

    @staticmethod
    def is_matching_passwords(password=None, re_password=None):
        return password == re_password
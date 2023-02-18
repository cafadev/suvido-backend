from rest_framework import serializers
from ..services import UserService


class UserSerializer(serializers.ModelSerializer):

    re_password = serializers.CharField(write_only=True)
    is_authenticated = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserService.model
        exclude = ['user_permissions', 'groups']
        extra_kwargs = {
            'id': { 'read_only': True },
            'password': { 'write_only': True },
            'username': { 'required': False },
            'last_login': { 'read_only': True },
            'date_joined': { 'read_only': True },
        }

    def validate(self, data):
        if 'password' in data and 're_password' in data:
            if UserService.is_matching_passwords(**data):
                raise serializers.ValidationError({ 're_password': ["Las contraseñas no coinciden"] })

        return data

    def create(self, validated_data):
        validated_data.pop('re_password')
        return UserService.create_user_or_superuser(validated_data)

    def update(self, instance, validated_data):
        UserService.update_user(instance, validated_data)
        return super().update(instance, validated_data)

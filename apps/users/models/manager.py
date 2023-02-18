from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_superuser(self, email, first_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, password, **extra_fields)

    def create_user(self, email, first_name, password, **extra_fields):
        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email).lower()
        user = self.model(email=email, first_name=first_name, **extra_fields)

        user.first_name = user.first_name.title()
        user.last_name = user.last_name.title()

        user.set_password(password)
        user.save()
        return user

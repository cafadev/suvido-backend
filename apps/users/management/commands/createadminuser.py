from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):

    help = 'Create the admin user'

    def add_arguments(self, parser):
        parser.add_argument('first_name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        user = User.objects.get_or_create(
            email=options.get('email'),
            first_name=options.get('first_name'),
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        if user[1]:
            user.set_password(options.get('password'))
            user.save()

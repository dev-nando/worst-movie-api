"""Comando que cria o superuser."""
from logging import getLogger

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

logger = getLogger("django")


class Command(BaseCommand):
    """Implementação do comando."""

    def handle(self, *args, **options) -> None:  # noqa: ANN002, ANN003, ARG002
        """Lógica do comando."""
        if not User.objects.filter(is_superuser=True):
            username = settings.DJANGO_SUPERUSER_USERNAME
            email = settings.DJANGO_SUPERUSER_EMAIL
            password = settings.DJANGO_SUPERUSER_PASSWORD
            User.objects.create_superuser(username, email, password)
            logger.info("Superuser criado!")
        else:
            logger.warning("Ja existem usuarios admin!")


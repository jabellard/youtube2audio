'''
from django.core.management.base import BaseCommand
from apps._admin.handlers import execute_delete_expired_texts


class Command(BaseCommand):

    def handle(self, *args, **options):
        execute_delete_expired_texts()
'''

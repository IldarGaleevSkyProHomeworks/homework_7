from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from app_users.apps import AppUsersConfig


class Command(BaseCommand):
    def handle(self, *args, **options):

        def print_group_status(group, name, status):
            print(f'{group} group "{name}" -', "created" if status else "exists")

        _, created_manager_group = Group.objects.get_or_create(name=AppUsersConfig.manager_group_name)
        print_group_status('Manager', AppUsersConfig.manager_group_name, created_manager_group)

        _, created_creator_group = Group.objects.get_or_create(name=AppUsersConfig.content_creator_group_name)
        print_group_status('Content creator', AppUsersConfig.content_creator_group_name, created_creator_group)


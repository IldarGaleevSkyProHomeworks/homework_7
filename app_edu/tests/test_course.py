import django.db.models.signals as django_orm_signals
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

import app_edu.signals as edu_signals
import app_payments.apps
from app_edu.models import Course
from app_users.apps import AppUsersConfig


class TestsCRUDCourse(TestCase):

    @classmethod
    def setUpClass(cls):
        edu_signals.course_post_create.disconnect(sender=Course, dispatch_uid=app_payments.apps.AppPaymentsConfig.name)
        edu_signals.course_post_update.disconnect(sender=Course, dispatch_uid=app_payments.apps.AppPaymentsConfig.name)
        django_orm_signals.pre_delete.disconnect(sender=Course, dispatch_uid=app_payments.apps.AppPaymentsConfig.name)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        moder_group, _ = Group.objects.get_or_create(name=AppUsersConfig.manager_group_name)
        creator_group, _ = Group.objects.get_or_create(name=AppUsersConfig.content_creator_group_name)

        self.moderator = get_user_model().objects.create(email='moder@a.com', password='1234')
        self.moderator.groups.add(moder_group)

        self.creator = get_user_model().objects.create(email='creator@a.com', password='1234')
        self.creator.groups.add(creator_group)

        self.user = get_user_model().objects.create(email='user@a.com', password='1234')

        self.user_owner = get_user_model().objects.create(email='owner@a.com', password='1234')

        self.user.save()
        self.moderator.save()
        self.creator.save()
        self.user_owner.save()

    def check_create_course(self, user, status_code):
        course_test_data = {'name': 'Test Course', 'description': 'Test Description'}
        self.client.force_login(user)
        url = reverse('app_edu:courses-list')
        response = self.client.post(url, data=course_test_data)
        self.assertEqual(response.status_code, status_code)

    def check_list_course(self, user, count):
        Course.objects.create(name=f'test', description='test', owner=self.user_owner)
        Course.objects.create(name=f'test', description='test', owner=self.user)
        Course.objects.create(name=f'test', description='test', owner=self.creator)

        self.client.force_login(user)
        url = reverse('app_edu:courses-list')
        response = self.client.get(url)
        result_count = response.json()['count']

        self.assertEqual(result_count, count)

    def check_retrieve_course(self, user, status_code):
        single_course = Course.objects.create(name='test', description='test', owner=self.user_owner)
        self.client.force_login(user)
        url = reverse('app_edu:courses-detail', args=[single_course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def check_update_course(self, user, status_code):
        single_course = Course.objects.create(name='test', description='test', owner=self.user_owner)
        self.client.force_login(user)
        url = reverse('app_edu:courses-detail', args=[single_course.pk])
        response = self.client.put(
            url,
            data={"name": "new_name", "description": "new"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status_code)

    def check_delete_course(self, user, status_code):
        deleted_course = Course.objects.create(name='test', description='test', owner=self.user_owner)
        self.client.force_login(user)
        url = reverse('app_edu:courses-detail', args=[deleted_course.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status_code)

    def test_create_moderator_forbidden(self):
        self.check_create_course(self.moderator, status.HTTP_403_FORBIDDEN)

    def test_create_creator_success(self):
        self.check_create_course(self.creator, status.HTTP_201_CREATED)

    def test_create_user_forbidden(self):
        self.check_create_course(self.user, status.HTTP_403_FORBIDDEN)

    def test_delete_moderator_forbidden(self):
        self.check_delete_course(self.moderator, status.HTTP_403_FORBIDDEN)

    def test_delete_owner_success(self):
        self.check_delete_course(self.user_owner, status.HTTP_204_NO_CONTENT)

    def test_delete_user_forbidden(self):
        self.check_delete_course(self.user, status.HTTP_403_FORBIDDEN)

    def test_delete_creator_no_owner_forbidden(self):
        self.check_delete_course(self.user, status.HTTP_403_FORBIDDEN)

    def test_list_owner_1(self):
        self.check_list_course(self.user_owner, 1)

    def test_list_moderator_3(self):
        self.check_list_course(self.moderator, 3)

    def test_list_creator_1(self):
        self.check_list_course(self.creator, 1)

    def test_retrieve_owner_success(self):
        self.check_retrieve_course(self.user_owner, status.HTTP_200_OK)

    def test_retrieve_moderator_success(self):
        self.check_retrieve_course(self.moderator, status.HTTP_200_OK)

    def test_retrieve_user_forbidden(self):
        self.check_retrieve_course(self.user, status.HTTP_403_FORBIDDEN)

    def test_update_owner_success(self):
        self.check_update_course(self.user_owner, status.HTTP_200_OK)

    def test_update_moderator_success(self):
        self.check_update_course(self.moderator, status.HTTP_200_OK)

    def test_update_user_forbidden(self):
        self.check_update_course(self.user, status.HTTP_403_FORBIDDEN)

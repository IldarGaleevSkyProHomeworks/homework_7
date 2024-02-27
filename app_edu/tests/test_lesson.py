from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from app_edu.models import Lesson
from app_users.apps import AppUsersConfig


class TestsCRUDLesson(TestCase):
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

    def check_create_lesson(self, user, status_code):
        lesson_test_data = {'name': 'Test lesson', 'description': 'Test Description'}
        self.client.force_login(user)
        url = reverse('app_edu:lesson_create')
        response = self.client.post(url, data=lesson_test_data)
        self.assertEqual(response.status_code, status_code)

    def check_list_lesson(self, user, count):
        Lesson.objects.create(name=f'test', description='test', owner=self.user_owner)
        Lesson.objects.create(name=f'test', description='test', owner=self.user)
        Lesson.objects.create(name=f'test', description='test', owner=self.creator)

        self.client.force_login(user)
        url = reverse('app_edu:lesson_list')
        response = self.client.get(url)
        result_count = response.json()['count']

        self.assertEqual(result_count, count)

    def check_retrieve_lesson(self, user, status_code):
        single_lesson = Lesson.objects.create(name='test', description='test', owner=self.user_owner)
        self.client.force_login(user)
        url = reverse('app_edu:lesson_detail', args=[single_lesson.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def check_update_lesson(self, user, status_code):
        single_lesson = Lesson.objects.create(name='test', description='test', owner=self.user_owner)
        self.client.force_login(user)
        url = reverse('app_edu:lesson_update', args=[single_lesson.pk])
        response = self.client.put(
            url,
            data={"name": "new_name", "description": "new"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status_code)

    def check_delete_lesson(self, user, status_code):
        deleted_lesson = Lesson.objects.create(name='test', description='test', owner=self.user_owner)
        self.client.force_login(user)
        url = reverse('app_edu:lesson_delete', args=[deleted_lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status_code)

    def test_create_moderator_forbidden(self):
        self.check_create_lesson(self.moderator, status.HTTP_403_FORBIDDEN)

    def test_create_creator_success(self):
        self.check_create_lesson(self.creator, status.HTTP_201_CREATED)

    def test_create_user_forbidden(self):
        self.check_create_lesson(self.user, status.HTTP_403_FORBIDDEN)

    def test_delete_moderator_forbidden(self):
        self.check_delete_lesson(self.moderator, status.HTTP_403_FORBIDDEN)

    def test_delete_owner_success(self):
        self.check_delete_lesson(self.user_owner, status.HTTP_204_NO_CONTENT)

    def test_delete_user_forbidden(self):
        self.check_delete_lesson(self.user, status.HTTP_403_FORBIDDEN)

    def test_delete_creator_no_owner_forbidden(self):
        self.check_delete_lesson(self.user, status.HTTP_403_FORBIDDEN)

    def test_list_owner_1(self):
        self.check_list_lesson(self.user_owner, 1)

    def test_list_moderator_3(self):
        self.check_list_lesson(self.moderator, 3)

    def test_list_creator_1(self):
        self.check_list_lesson(self.creator, 1)

    def test_retrieve_owner_success(self):
        self.check_retrieve_lesson(self.user_owner, status.HTTP_200_OK)

    def test_retrieve_moderator_success(self):
        self.check_retrieve_lesson(self.moderator, status.HTTP_200_OK)

    def test_retrieve_user_forbidden(self):
        self.check_retrieve_lesson(self.user, status.HTTP_403_FORBIDDEN)

    def test_update_owner_success(self):
        self.check_update_lesson(self.user_owner, status.HTTP_200_OK)

    def test_update_moderator_success(self):
        self.check_update_lesson(self.moderator, status.HTTP_200_OK)

    def test_update_user_forbidden(self):
        self.check_update_lesson(self.user, status.HTTP_403_FORBIDDEN)

    def test_create_with_bad_video_url_bad_request(self):
        lesson_test_data = {
            'name': 'Test lesson',
            'description': 'Test Description',
            'video_url': 'https://mysupersite.com/coolvideo'
        }
        self.client.force_login(self.creator)
        url = reverse('app_edu:lesson_create')
        response = self.client.post(url, data=lesson_test_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def check_create_with_youtube_video_url(self, url):
        lesson_test_data = {
            'name': 'Test lesson',
            'description': 'Test Description',
            'video_url': url
        }
        self.client.force_login(self.creator)
        url = reverse('app_edu:lesson_create')
        response = self.client.post(url, data=lesson_test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_with_youtube_video_1_url_success(self):
        self.check_create_with_youtube_video_url('https://youtu.be/qwerty123')

    def test_create_with_youtube_video_2_url_success(self):
        self.check_create_with_youtube_video_url('https://www.youtube.com/watch?v=qwerty123')

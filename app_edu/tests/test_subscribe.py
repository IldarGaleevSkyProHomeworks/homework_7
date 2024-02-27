from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from app_edu.models import Course


class TestsSubscription(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email='moder@a.com', password='1234')
        self.course = Course.objects.create(name='course', description='d')

    def test_subscribe_anon_unauthorized(self):
        url = reverse('app_edu:subscribe', args=[self.course.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_user_success(self):
        self.client.force_login(self.user)
        url = reverse('app_edu:subscribe', args=[self.course.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscribe_to_not_exist_anon_unauthorized(self):
        url = reverse('app_edu:subscribe', args=[999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_to_not_exist_user_notfound(self):
        self.client.force_login(self.user)
        url = reverse('app_edu:subscribe', args=[999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unsubscribe_anon_unauthorized(self):
        url = reverse('app_edu:subscribe', args=[self.course.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unsubscribe_user_success(self):
        self.client.force_login(self.user)
        url = reverse('app_edu:subscribe', args=[self.course.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unsubscribe_to_not_exist_anon_unauthorized(self):
        url = reverse('app_edu:subscribe', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unsubscribe_to_not_exist_user_notfound(self):
        self.client.force_login(self.user)
        url = reverse('app_edu:subscribe', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

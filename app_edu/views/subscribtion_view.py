from rest_framework import status
from rest_framework import views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app_edu.models import Course, Subscription
from app_edu.serializers import SubscriptionSerializer


class SubscribeUnsubscribeAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])

        subs, _ = Subscription.objects.get_or_create(user=self.request.user, course=course)
        serializer = SubscriptionSerializer(subs)
        response = {
            'results': serializer.data,
            'detail': f'Курс {course.name} сохранен в подписки'
        }
        return Response(response, status.HTTP_201_CREATED)

    def delete(self, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        Subscription.objects.filter(user=self.request.user, course=course).delete()
        response = {
            'detail': f'Курс {course.name} удален из подписок',
        }
        return Response(response, status.HTTP_204_NO_CONTENT)

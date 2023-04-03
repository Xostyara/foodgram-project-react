from rest_framework import serializers
from rest_framework.serializers import Serializer

from users.models import Follow


class IsSubscribedMixin(Serializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, data):
        user = self.context.get('request').user 
        if user.is_anonymous: 
            return False 
        return Follow.objects.filter(user=user, author=user).exists() 

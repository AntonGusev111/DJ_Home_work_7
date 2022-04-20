from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)
        read_only_fields = ['username']


class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        request = self.context.get('request', None)
        open_adv = Advertisement.objects.filter(creator_id=request.user.id, status='OPEN')
        if len(open_adv) >= 10 and request.method == 'POST' or len(open_adv) >= 10 and request.data.get(
                'status') == 'OPEN':
            raise ValidationError('Too many open adv')
        return data

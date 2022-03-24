from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from base.models import router_details


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'token', 'first_name']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = router_details
        fields = '__all__'

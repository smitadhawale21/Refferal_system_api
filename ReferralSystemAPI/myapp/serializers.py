from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'referral_code', 'timestamp']

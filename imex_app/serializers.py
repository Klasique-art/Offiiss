from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    license = serializers.ImageField(required=False)
    image = serializers.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ['id', 'user', 'user_id', 'name', 'telephone_number', 'image', 'license', 'user_type', 'company', 'company_description', 'company_location',  'city', 'region', 'agent_type', 'agent_status']


class ImageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    image = serializers.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ["id", "image", "user_id", "user"]

from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id","email","first_name","last_name","username"]
    

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    
    image = serializers.ImageField(required = False,)
    class Meta:
        model = Profile
        fields = ['id', 'user', 'user_id', 'name', 'telephone_number', 'image',]



class ImageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    image = serializers.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ["id", "image", "user_id", "user"]



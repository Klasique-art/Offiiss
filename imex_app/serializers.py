from rest_framework import serializers
from .models import Agent, AgentReview, Profile,Transporter,TransporterReview
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Max, Q, Sum


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id","email","first_name","last_name","username"]
    

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    email = serializers.ReadOnlyField(source="user.email")
    
    image = serializers.ImageField(required = False,)
    class Meta:
        model = Profile
        fields = ['id', 'user', 'user_id', 'name', 'telephone_number', 'image','email']



class ImageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    image = serializers.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ["id", "image", "user_id", "user"]


class AgentSerializer(serializers.ModelSerializer):
    num_reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = ['id', 'user', 'agent_name', 'agent_phone','category','company_name', 'location','description', 'profile_image','license','rating','num_reviews','cover_image','created_at','updated_at','status']
    def get_num_reviews(sef,obj):
        try:
            return obj.user.reviews.aggregate(Count('rating'))['rating__count']
        except TypeError:
            return 0
    def get_rating(sef,obj):
        try:
            return obj.user.reviews.aggregate(Sum('rating'))['rating__sum']/obj.user.reviews.aggregate(Count('rating'))['rating__count']
        except TypeError:
            return 0.0
    
class TransporterSerializer(serializers.ModelSerializer):
    num_reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    class Meta:
        model = Transporter
        fields = ['id', 'user', 'driver_name', 'driver_phone', 'location','description', 'profile_image','driver_license_number',"trailer_axle","triiler_type","triiler_length","trucks_plate_number",
            "license_number","trailer_license_plate",'rating','num_reviews','vehicle_1','vehicle_2','vehicle_3','vehicle_4','created_at','updated_at','status']
    def get_num_reviews(sef,obj):
        try:
            return obj.user.reviews.aggregate(Count('rating'))['rating__count']
        except TypeError:
            return 0
    def get_rating(sef,obj):
        try:
            return obj.user.reviews.aggregate(Sum('rating'))['rating__sum']/obj.user.reviews.aggregate(Count('rating'))['rating__count']
        except TypeError:
            return 0.0
    

class AgentReviewSerializer(serializers.ModelSerializer):
    client_profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = AgentReview
        fields = ["id","agent","client","client_profile","content","rating"]
    def get_client_profile(self,obj):
        # profile = Profile.objects.get(pk=obj.client)
        serializer = ProfileSerializer(obj.client)
        return serializer.data
class TransporterReviewSerializer(serializers.ModelSerializer):
    client_profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = TransporterReview
        fields = ["id","transporter","client","client_profile","content","rating"]
    def get_client_profile(self,obj):
        # profile = Profile.objects.get(pk=obj.client)
        serializer = ProfileSerializer(obj.client)
        return serializer.data
class LoginDataSerializer(serializers.Serializer):
    
    refresh = serializers.CharField()
    access = serializers.CharField()
    email = serializers.EmailField()
    name = serializers.CharField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profile_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    telephone_number = serializers.CharField()
    image = serializers.CharField()
    
        
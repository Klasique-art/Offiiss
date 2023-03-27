from .models import Profile
from rest_framework import viewsets
from .serializers import ImageSerializer, ProfileSerializer,UserSerializer
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
   

    def create(self, request):
        
        data = request.data
        print(data)
       
        serializer = UserSerializer(data=data)
        if User.objects.filter(email=data['email']).exists():
                return Response({'status': "A user with the specified email already exists"}, status=status.HTTP_409_CONFLICT)
        else:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user.password = make_password(data['password'])
            user.username = data["email"]
            user.save()
            user_profile = Profile.objects.create(user = user,telephone_number = data["telephone_number"])
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
    def retrieve(self, request, pk=None):
        user = get_object_or_404(User,pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":"Updated"},status=status.HTTP_200_OK)

    

    def destroy(self, request, pk=None):
        user = get_object_or_404(User,pk=pk)
        user.delete()
        return Response({'status': "Success"})
    
    
         



    

class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
#    permission_classes = [
#        permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class ImageView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser, FormParser)
#    permission_classes = [
#        permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




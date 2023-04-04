from .models import Profile,Agent,Transporter
from rest_framework import viewsets
from .serializers import ImageSerializer, ProfileSerializer,UserSerializer,AgentSerializer,TransporterSerializer
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .pagination import StandardResultsSetPagination
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

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    parser_classes = (MultiPartParser,FormParser)
    pagination_class = StandardResultsSetPagination
   
    # http_method_names = ['get', 'post']


    def list(self,request):
        category = request.GET.get("category",None)
        if category == "seaport":
            query_set = self.queryset.filter(category = 1)
        elif category == "airport":
            query_set = self.queryset.filter(category = 2)
        else:
            query_set = self.queryset
        
        results = self.paginate_queryset(query_set)
        serializer = self.serializer_class(results,many=True,context= 
        {'request': request})
        return self.get_paginated_response(serializer.data)
    
    def create(self, request, *args, **kwargs):

        data = request.data
        try:

            user = User.objects.get(pk=data["user"])
            
            # agent = Agent(user=user,agent_phone =data["agent_phone"],company_name = data["company_name"],location=data["location"],agent_name = data["agent_name"],description = data["description"],license = data["license"],category = data["category"])
            # agent.save()
            serializer = self.serializer_class(data=data,context={"agent":user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransporterViewSet(viewsets.ModelViewSet):
    queryset = Transporter.objects.all()
    serializer_class = TransporterSerializer
    parser_classes = (MultiPartParser,FormParser)
    pagination_class = StandardResultsSetPagination
   
    # http_method_names = ['get', 'post']


    def list(self,request):
        # category = request.get("category",None)
        query_set = Transporter.objects.filter()
        results = self.paginate_queryset(query_set)
        serializer = self.serializer_class(results,many=True,context= 
        {'request': request})
        return self.get_paginated_response(serializer.data)
    
    def create(self, request, *args, **kwargs):

        data = request.data
        try:

            user = User.objects.get(pk=data["user"])
            
            # agent = Transporter(user=user,agent_phone =data["agent_phone"],company_name = data["company_name"],location=data["location"],agent_name = data["agent_name"],description = data["description"],license = data["license"],category = data["category"])
            # agent.save()
            serializer = self.serializer_class(data=data,context={"transporter":user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
            

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




from .models import Profile,Agent,Transporter,AgentReview,TransporterReview
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import AgentReviewSerializer,TransporterReviewSerializer, ImageSerializer, ProfileSerializer,UserSerializer,AgentSerializer,TransporterSerializer
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .pagination import StandardResultsSetPagination
from django.db.models import Q

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
            user_profile = Profile.objects.create(user = user,telephone_number = data["telephone_number"],name = data["name"])
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

class AgentReviewViewSet(viewsets.ViewSet):
    serializer_class = AgentReviewSerializer
    queryset = AgentReview.objects.all()
    def create(self,request,*args, **kwargs):
        data = request.data
        
        serializer = self.serializer_class(data=data)
            
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        agent = Agent.objects.get(pk=request.GET.get("agent",None))
        queryset = self.queryset.filter(agent=agent)
        serializer = self.serializer_class(queryset,many=True,context={"request":request})
        return Response(serializer.data)


class TransporterReviewViewSet(viewsets.ViewSet):
    serializer_class = TransporterReviewSerializer
    queryset = TransporterReview.objects.all()
    def create(self,request,*args, **kwargs):
        data = request.data
        
        serializer = self.serializer_class(data=data)
            
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        transporter = Transporter.objects.get(pk=request.GET.get("transporter",None))
        queryset = self.queryset.filter(transporter=transporter)
        serializer = self.serializer_class(queryset,many=True)
        return Response(serializer.data)
        



class SearchView(APIView):
    def get(self,request):
        query = request.GET.get('query',None)
        agents = Agent.objects.filter(Q(agent_name__contains = query)| Q(company_name__contains = query) | Q(location__contains = query))
        transporters = Transporter.objects.filter(Q(driver_name__contains = query) | Q(location__contains = query))

        
        
        return Response({"agents":AgentSerializer(agents,many=True,context= 
        {'request': request}).data,"transporters":TransporterSerializer(transporters,many=True,context= 
        {'request': request}).data})

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




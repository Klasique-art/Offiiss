from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Profile, Review, AgentType
from django.db.models import Count, Avg, Max, Q, Sum
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


@api_view(['GET'])
def agents(request):
    if request.GET.get('agent_type'):
        agent_type = AgentType.objects.get(slug = request.GET.get('agent_type'))
        agents = Profile.objects.filter(agent_type = agent_type, is_agent=True)
        paginate_obj = Paginator(agents, 10)
        results = paginate_obj.get_page(int(request.GET.get("page", 1)))
        data = [{"agent_id": agent.user_id, "name": agent.name, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.user.reviews.aggregate(Sum('rating'))['rating__sum'],'num_reviews':agent.user.reviews.aggregate(Count('rating'))['rating__count'], "city": agent.city, "region": agent.region, "company_location": agent.company_location} for agent in results]
        # data.append({"pagination_info": {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}})
        return Response({'objects':data,"pagination_info": {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}})
    else:
        agents = Profile.objects.filter(is_agent=True)[:request.GET.get('limit')]
        paginate_obj = Paginator(agents, 10)
        results = paginate_obj.get_page(int(request.GET.get("page", 1)))
        data = [{"agent_id": agent.user_id, "name": agent.name, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.user.reviews.aggregate(Sum('rating'))['rating__sum'],'num_reviews':agent.user.reviews.aggregate(Count('rating'))['rating__count'], "city": agent.city, "region": agent.region, "company_location": agent.company_location} for agent in results]
        # data.append({"pagination_info": {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}})
#            data = [{"agent_id": agent.id, "name": agent.name, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.reviews.aggregate(Sum('rating'))['rating__sum'], "city": agent.city, "region": agent.region, "company_location": agent.company_location} for agent in agents]            
        return Response({'objects':data,"pagination_info": {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}})

@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        try:
            username = request.data.get('username')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            email = request.data.get('email')
            password = request.data.get('password')
            if User.objects.filter(username=username).exists():
                return Response({'status': "User already exists"}, status=status.HTTP_409_CONFLICT)
            else:
                user = User.objects.create(email=email, password=make_password(password), first_name=first_name, last_name=last_name, username=username)
                Profile.objects.create(user=user, is_client=True)
                return Response({"status": "Account created"})
        except Exception as e:
            return Response({'status': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# api view to create a client

@api_view(['POST'])
def create_agent(request):
    if request.method == 'POST':
        try:
            username = request.data.get('username')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            email = request.data.get('email')
            password = request.data.get('password')
            if User.objects.filter(username=username).exists():
                return Response({'status': "User already exists"}, status=status.HTTP_409_CONFLICT)
            else:
                user = User.objects.create(email=email, password=make_password(password), first_name=first_name, last_name=last_name, username=username, is_active=True)
                Profile.objects.create(user=user, is_agent=True)
                return Response({"status": "Account created"})
        except Exception as e:
            return Response({'status': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# api view to create agent

@api_view(['POST'])
def change_email(request):
    pass

@api_view(['POST'])
def change_password(request):
    pass

@api_view(["POST"])
def create_profile(request):
    if request.method == "POST":
        name = request.data.get("name")
        telephone_number = request.data.get("telephone_number")
        company = request.data.get("company")
        company_description = request.data.get("company_description")
        company_location = request.data.get("company_location")
        city = request.data.get("city")
        region = request.data.get("region")
        user_id = request.data.get("user_id")
        agent_type = request.data.get("agent_type")
        Profile.objects.create(name=name, telephone_number=telephone_number, company=company, company_description=company_description, company_location=company_location, city=city, region=region, user_id=user_id, agent_type_id=agent_type, is_agent=True)
        return Response({"status": "Profile created"})

class MyTokenObtainPair(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # serializer = UserSerializerWithToken(self.user).data
        # for k,v in serializer.items():
        # data[k] = v
        user_profile = Profile.objects.get(user = self.user)
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['name'] = user_profile.name
        data['is_agent'] = user_profile.is_agent
        data['agent_status'] = user_profile.agent_status
        return data
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPair


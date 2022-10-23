from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Profile, Review, AgentType
from django.db.models import Count, Avg, Max, Q, Sum
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password

@api_view(['GET'])
def agents(request):
    if request.GET.get('agent_type'):
        agents = Profile.objects.filter(agent_type__type=request.GET.get('agent_type'), is_agent=True)
        paginate_obj = Paginator(agents, 10)
        results = paginate_obj.get_page(int(request.GET.get("page", 1)))
        data = [{"agent_id": agent.user_id, "name": agent.name, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.user.reviews.aggregate(Sum('rating'))['rating__sum'], "city": agent.city, "region": agent.region, "company_location": agent.company_location} for agent in results]
        data.append({"pagination_info": {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}})
        return Response(data)
    else:
        agents = Profile.objects.filter(is_agent=True)[:request.GET.get('limit')]
        paginate_obj = Paginator(agents, 10)
        results = paginate_obj.get_page(int(request.GET.get("page", 1)))
        data = [{"agent_id": agent.user_id, "name": agent.name, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.user.reviews.aggregate(Sum('rating'))['rating__sum'], "city": agent.city, "region": agent.region, "company_location": agent.company_location} for agent in results]
        data.append({"pagination_info": {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}})
#            data = [{"agent_id": agent.id, "name": agent.name, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.reviews.aggregate(Sum('rating'))['rating__sum'], "city": agent.city, "region": agent.region, "company_location": agent.company_location} for agent in agents]            
        return Response(data)

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



# view to create profile for agents.

@api_view(["POST"])
def review(request):
    if request.method == "	POST":
        name = request.data.get("name")
        content = request.data.get("content")
        agent_id = request.data.get("agent_id")
        Review.objects.create(name=name, content=content, user_id=agent_id)
        return Response({"status": "created"})
    else:
        agent_id = request.GET.get("agent_id")
        reviews = Review.objects.filter(user_id=agent_id)
        paginate_obj = Paginator(reviews, 10)
        results = paginate_obj.get_page(int(request.GET.get("page", 1)))
        data = [{"name": review.name, "content": review.content} for review in results]
        data.append({"pagination_info": {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}})
        return Response(data)

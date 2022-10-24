from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Agent, AgentType, Review
from django.db.models import Count, Avg, Max, Q, Sum
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


@api_view(['GET', 'POST', 'DELETE'])
def agents(request):
    if request.method == 'POST':
        agent_id = request.data.get('agent_id')
        name = request.data.get('name')
        content = request.data.get('content')
        rating = request.data.get('rating')
        agent = get_object_or_404(Agent, pk=agent_id)
        Review.objects.create(name=name, agent=agent, rating=rating, content=content)
        return Response({"status": "created"})
    else:
        if request.GET.get('agent_type'):
            agent_type = AgentType.objects.get(slug = request.GET.get('agent_type'))
            agents = Agent.objects.filter(agent_type=agent_type).annotate(re=Avg('reviews__rating')).order_by('-re')
            paginate_obj = Paginator(agents, 6)
            results = paginate_obj.get_page(int(request.GET.get("page",1)))
            data = [{"agent_id": agent.id, "name": agent.name,'num_reviews':agent.reviews.aggregate(Count('rating'))['rating__count'],'image':agent.image.url, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.reviews.aggregate(Avg('rating'))['rating__avg'], "city": agent.city, "region": agent.region, "company_location": agent.company_location} for agent in results]
            pagination_info =  {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}
#            data = [{"agent_id": agent.id, "name": agent.name, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.reviews.aggregate(Sum('rating'))['rating__sum'], "city": agent.city, "region": agent.region, "company_location": agent.company_location} for agent in agents]            
            return Response({'objects':data,'pagination_info':pagination_info})

        else:
            agents = Agent.objects.annotate(re=Avg('reviews__rating')).order_by('-re')[:int(request.GET.get("limit", int(Agent.objects.count())-1))]
            paginate_obj = Paginator(agents, 6)
            results = paginate_obj.get_page(int(request.GET.get("page", 1)))
            data = [{"agent_id": agent.id, "name": agent.name,'num_reviews':agent.reviews.aggregate(Count('rating'))['rating__count'],'image':agent.image.url, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.reviews.aggregate(Avg('rating'))['rating__avg'], "city": agent.city, "region": agent.region, "company_location": agent.company_location} for agent in results]
            pagination_info =  {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}
#            data = [{"agent_id": agent.id, "name": agent.name, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.reviews.aggregate(Sum('rating'))['rating__sum'], "city": agent.city, "region": agent.region, "company_location": agent.company_location} for agent in agents]            
            return Response({'objects':data,'pagination_info':pagination_info})

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
                User.objects.create(email=email, password=make_password(password), first_name=first_name, last_name=last_name, username=username)
                return Response({"status": "Account created"})
        except Exception as e:
            return Response({'status': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MyTokenObtainPair(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # serializer = UserSerializerWithToken(self.user).data
        # for k,v in serializer.items():
        # data[k] = v
        
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        return data
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPair
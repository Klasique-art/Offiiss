from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Profile, Review, AgentType,Order
from django.db.models import Count, Avg, Max, Q, Sum
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET'])
def agents(request):
    if request.GET.get('agent_type'):
        # agent_type = AgentType.objects.get(slug = request.GET.get('agent_type'))
        agent_type = request.GET.get('agent_type')
        if agent_type == 'sea-port':
            agents = Profile.objects.filter(user_type = 2,agent_status = 3,is_sea_port = True)
        else:
            agents = Profile.objects.filter(user_type = 2,agent_status = 3,is_air_port = True)
        paginate_obj = Paginator(agents, 10)
        results = paginate_obj.get_page(int(request.GET.get("page", 1)))
        data = [{"agent_user_id":agent.user_id, "agent_id": agent.id, "name": agent.name, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.user.reviews.aggregate(Sum('rating'))['rating__sum'],'num_reviews':agent.user.reviews.aggregate(Count('rating'))['rating__count'], "city": agent.city, "region": agent.region, "company_location": agent.company_location,'image':agent.image.url,'is_air_port':agent.is_air_port,'is_sea_port':agent.is_sea_port} for agent in results]
        # data.append({"pagination_info": {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}})
        return Response({'objects':data,"pagination_info": {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}})
    else:
        agents = Profile.objects.filter(user_type = 2,agent_status = 3)[:request.GET.get('limit')]
        paginate_obj = Paginator(agents, 10)
        results = paginate_obj.get_page(int(request.GET.get("page", 1)))
        data = [{"agent_user_id":agent.user_id,"agent_id": agent.id, "name": agent.name, "telephone_number": agent.telephone_number, "type": agent.agent_type.type, "company": agent.company, "company_description": agent.company_description, "rating": agent.user.reviews.aggregate(Sum('rating'))['rating__sum'],'num_reviews':agent.user.reviews.aggregate(Count('rating'))['rating__count'], "city": agent.city, "region": agent.region, "company_location": agent.company_location,'image':agent.image.url,'is_air_port':agent.is_air_port,'is_sea_port':agent.is_sea_port} for agent in results]

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
                return Response({'status': "A user with the specified username already exists"}, status=status.HTTP_409_CONFLICT)
            if User.objects.filter(email=email).exists():
                return Response({'status': "User with the specified Email already exists"}, status=status.HTTP_409_CONFLICT)

            else:
                user = User.objects.create(email=email, password=make_password(password), first_name=first_name, last_name=last_name, username=username)
                user_profile = Profile.objects.create(user=user,user_type = 1,name=user.first_name + ' ' + user.last_name)
                return Response({"status": "Account created","profile_id":user_profile.id})
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

                return Response({'status': "User with the specified Username already exists"}, status=status.HTTP_409_CONFLICT)
            if User.objects.filter(email=email).exists():
                return Response({'status': "User with the specified Email already exists"}, status=status.HTTP_409_CONFLICT)

            else:
                user = User.objects.create(email=email, password=make_password(password), first_name=first_name, last_name=last_name, username=username, is_active=True)
                user_profile = Profile.objects.create(user=user, user_type=2,name=user.first_name + ' ' + user.last_name)
                return Response({"status": "Account created","profile_id":user_profile.id})
        except Exception as e:
            return Response({'status': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# api view to create agent

@api_view(["POST"])
def change_email(request):
    if request.method == "POST":
        user_id = request.data.get("user_id")
        email= request.data.get("email")
        if User.objects.filter(email=email).exists():
                return Response({'status': "User already exists"}, status=status.HTTP_409_CONFLICT)
        user = get_object_or_404(User, pk=user_id)
        user.email = email
        user.save()
        return Response({"status": "changed"})

@api_view(['POST'])
def change_password(request):
    if request.method == "POST":
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        password = request.data.get("password")
        user.password = make_password(password)
        user.save()
        return Response({"status": "changed"})

@api_view(['POST'])
def reset_password(request):
    if request.method == "POST":
        user_email = request.data.get("email")
        user = get_object_or_404(User, email=user_email)
        password = request.data.get("password")
        user.password = make_password(password)
        user.save()
        return Response({"status": "changed"})

@api_view(["POST"])
def change_username(request):
    if request.method == "POST":
        user_id = request.data.get("user_id")
        user_name= request.data.get("username")
        if User.objects.filter(username=user_name).exists():
                return Response({'status': "User already exists"}, status=status.HTTP_409_CONFLICT)
        user = get_object_or_404(User, pk=user_id)
        user.username = user_name
        user.save()
        return Response({"status": "changed"})

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
@api_view(['GET','POST'])
def reviews(request):
    if request.method == "POST":
        agent = User.objects.get(id = request.data.get('agent_id'))
        client = User.objects.get(id = request.data.get('client_id'))
        content = request.data.get('content')
        rating = request.data.get('rating')
        Review.objects.create(agent = agent,client = client,content=content,rating=rating)
        return Response({'status':'Review Created Successfully'})
    else:
        agent = User.objects.get(id = request.GET.get('agent_id'))
        reviews = Review.objects.filter(agent = agent)
        data = [{'agent_id':review.agent.id,'client_id':review.client.id,'client_name':f'{review.client.first_name} {review.client.last_name}','content':review.content,'rating':review.rating,'date':review.date} for review in reviews]
        return Response(data)


@api_view(["GET"])
def orders(request):
    # There is no field called user in order field and no telephone in user field
    agent_id = request.GET.get("agent_id")
    orders = Order.objects.filter(agent__pk=agent_id, is_done=False).all()
# there should be date
    data = [{"id":order.id,"client_name": f"{order.client.first_name} {order.client.last_name}","is_done":order.is_done, "date": order.date} for order in orders]
    return Response(data)

@api_view(["GET"])
def get_order(request,agent_id,client_id):

    try:
        Order.objects.get(agent__pk=agent_id,client__pk=client_id,is_done=False)
        return Response({"status": "Already exists"}, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

    except ObjectDoesNotExist:
        return Response({"status": "Does not exist"})


class MyTokenObtainPair(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # serializer = UserSerializerWithToken(self.user).data
        # for k,v in serializer.items():
        # data[k] = v
        user_profile = Profile.objects.get(user = self.user)
        data['profile_id'] = user_profile.id
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['name'] = user_profile.name
        data['user_type'] = user_profile.get_user_type_display()
        data['image'] = user_profile.image.url
        data['agent_status'] = user_profile.get_agent_status_display()
        data['is_email_validated'] = user_profile.is_validated
        return data
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPair


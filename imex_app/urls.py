from django.urls import path,include
from . views import (MyTokenObtainPairView, agents,create_user,MyTokenObtainPair,reviews, 
	create_agent, change_password, change_email, change_username, orders,get_order,reset_password,delete_user)
# from imex_app.api import ReviewResource as rr
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_view import ProfileView, ImageView,UserViewSet,AgentViewSet,TransporterViewSet
from  .order import check_code, order, done
from . import validate
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user-view', UserViewSet)
router.register(r'agent-view',AgentViewSet)
router.register(r'transporter-view',TransporterViewSet)
urlpatterns = [
path('profile/<int:pk>/', ProfileView.as_view({"post": "update"}), name='profile'),
path("image/<int:pk>/", ImageView.as_view({"post": "update"}), name="image"),
path('create-user/', create_user, name='create_user'),
path('delete-user/', delete_user, name='delete_user'),
path('create-agent/', create_agent, name='create_agent'),
path('change-username/', change_username, name='change_username'),
path('change-email/', change_email, name='change_email'),
path('change-password/', change_password, name='change_password'),
path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
path('agents/', agents, name='agents'),
path('reviews/',reviews,name = 'reviews' ),
path('order/check-code/', check_code, name='check_code'),
path('order/done/', done, name='order_done'),
path("fetch-orders/", orders, name='orders'),
path('order/', order, name='order'),
path("generate/", validate.generate, name='generate'),
path("validate-code/", validate.validate_code, name='validate_code'),
path("generate-email-code/", validate.generate_email_code, name='email_code'),
path("verify-email/", validate.verify_email, name='verify_email'),
path("reset/", validate.reset, name='reset'),
path('get-order/<int:agent_id>/<int:client_id>/', get_order, name='get_order'),
path('reset-password/',reset_password,name='reset_password'),
path('', include(router.urls)),
]

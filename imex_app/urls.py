from django.urls import path
from . views import MyTokenObtainPairView, agents,create_user,MyTokenObtainPair,reviews, create_agent, change_password, change_email, change_username, orders,get_order
# from imex_app.api import ReviewResource as rr
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . api import ProfileView, ImageView
from  .order import check_code, order, done
from . import validate

urlpatterns = [
path('profile/<int:pk>/', ProfileView.as_view({"post": "update"}), name='profile'),
path("image/<int:pk>/", ImageView.as_view({"post": "update"}), name="image"),
path('create-user/', create_user, name='create_user'),
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
<<<<<<< HEAD
path("generate/", validate.generate, name='generate'),
path("validate-code/", validate.validate_code, name='validate_code'),
path("reset/", validate.reset, name='reset'),
=======
path('get-order/<int:agent_id>/<int:client_id>/', get_order, name='get_order'),
>>>>>>> a6ed431fff67ce45bc8b59cf154c3eee8a658ff0
]

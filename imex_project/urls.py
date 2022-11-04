from django.contrib import admin
from django.urls import path, include
from imex_app.views import MyTokenObtainPairView, agents,create_user,MyTokenObtainPair,reviews, create_agent, change_password, change_email, change_username
# from imex_app.api import ReviewResource as rr
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# review = rr()
from imex_app.api import ProfileView, ImageView

urlpatterns = [
path('profile/<int:pk>/', ProfileView.as_view({"post": "update"}), name='profile'),
path("image/<int:pk>/", ImageView.as_view({"post": "update"}), name="image"),
 path('create-user/', create_user, name='create_user'),
path('change-username/', change_username, name='change_username'),
path('change-email/', change_email, name='change_email'),
path('change-password/', change_password, name='change_password'),
path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# path('api/', include(review.urls)),
path('agents/', agents, name='agents'),
path('admin/', admin.site.urls),
path('reviews/',reviews,name = 'reviews' )
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

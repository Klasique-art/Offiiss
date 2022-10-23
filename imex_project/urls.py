from django.contrib import admin
from django.urls import path, include
from imex_app.views import agents,create_user
from imex_app.api import ReviewResource as rr
from django.conf.urls.static import static
#from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
review = rr()

urlpatterns = [
path('create-user/', create_user, name='create_user'),
path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
path('api/', include(review.urls)),
path('agents/', agents, name='agents'),
path('admin/', admin.site.urls),
]
#urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

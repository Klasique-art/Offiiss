from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home.views import home_page, terms, privacy

urlpatterns = [
path('', home_page, name='home'),
path('privacy/', privacy, name='privacy'),
path('terms/', terms, name='terms'),
path('admin/', admin.site.urls),
path('offis-api/', include('imex_app.urls')),
]
if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

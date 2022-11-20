from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home.views import terms, privacy
from home.blog_views import home_page, letter, search
from home import feeds
from django.contrib.sitemaps.views import sitemap # new
from home.sitemap import BlogSitemap

maps = {"blog": BlogSitemap}


urlpatterns = [
    path('feed/', feeds.LatestPostsFeed(), name='feed'),
path('search/', search, name='search'),
path('letter/', letter, name='letter'),
path('', home_page, name='home'),
path('privacy/', privacy, name='privacy'),
path('terms/', terms, name='terms'),
path('admin/', admin.site.urls),
path('offis-api/', include('imex_app.urls')),
    path('sitemap.xml', sitemap, # new
        {'sitemaps': maps},
        name='django.contrib.sitemaps.views.sitemap'),

]
if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

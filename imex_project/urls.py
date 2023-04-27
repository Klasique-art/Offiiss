from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home.views import terms, privacy, read
from home.blog_views import home_page, letter, search, detail
from home import feeds
from django.contrib.sitemaps.views import sitemap # new
from home.sitemap import BlogSitemap

maps = {"blog": BlogSitemap}
from home import blog_views


urlpatterns = [
path('tag/<slug:tag_slug>/', blog_views.tags, name='post_list_by_tag'),
path('like/', blog_views.like, name='like'),
path("comment/", blog_views.comment, name="comment"),
path('detail/<int:pk>/<slug:slug>/', detail, name='detail'),
path('feed/', feeds.LatestPostsFeed(), name='feed'),
path('search/', search, name='search'),
path('letter/', letter, name='letter'),
path('', home_page, name='home'),
path('privacy/', privacy, name='privacy'),
path('read/', read, name="security"),
path('terms/', terms, name='terms'),
path('admin/', admin.site.urls),
path('sewonet_apis/offiiss_api/api_v1/', include('imex_app.urls'),),
path('sitemap.xml', sitemap, # new
        {'sitemaps': maps},
        name='django.contrib.sitemaps.views.sitemap'),
path('chat/',include('chat.urls'),name='chat'),
]

if settings.DEBUG:
  urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

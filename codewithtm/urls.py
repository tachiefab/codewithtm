"""codewithtm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="codewithtm API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://codewithtm-58c9d.web.app/",
        contact=openapi.Contact(email="codewithtm@gmail.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/about-us/', include('aboutus.urls', namespace='api-about-us')),
    path('api/analytics/', include('analytics.urls', namespace='api-analytics')),
    path('api/auth/', include('accounts.urls', namespace='api-auth')),
    path('api/author/', include('authors.urls', namespace='api-author')),
    path('api/categories/', include("categories.urls", namespace='categories-api')),
    path('api/comments/', include("comments.urls", namespace='comments-api')),
    path('api/faqs/', include('faqs.urls', namespace='api-faqs')),
    # path('api/likes/', include('likes.urls', namespace='api-likes')),
    path('api/posts/', include('posts.urls', namespace='api-posts')),
    path('api/contact-us/', include('reachus.urls', namespace='api-reachus')),
    path('api/tags/', include('tags.urls', namespace='api-tags')),
    path('api/user/', include('accounts.user.urls', namespace='api-user')),
    path('api/user/profile/', include('profiles.urls', namespace='api-profiles')),

    # third party
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
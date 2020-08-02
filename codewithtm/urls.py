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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/about-us/', include('aboutus.urls', namespace='api-about-us')),
    path('api/analytics/', include('analytics.urls', namespace='api-analytics')),
    path('api/auth/', include('accounts.urls', namespace='api-auth')),
    path('api/author/', include('authors.urls', namespace='api-author')),
    path('api/categories/', include("categories.urls", namespace='categories-api')),
    path('api/comments/', include("comments.urls", namespace='comments-api')),
    path('api/faqs/', include('faqs.urls', namespace='api-faqs')),
    path('api/posts/', include('posts.urls', namespace='api-posts')),
    path('api/tags/', include('tags.urls', namespace='api-tags')),
    path('api/user/', include('accounts.user.urls', namespace='api-user')),
    path('api/user/profile/', include('profiles.urls', namespace='api-profiles')),

    # third party
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
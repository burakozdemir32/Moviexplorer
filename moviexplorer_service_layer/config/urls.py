"""moviexplorer_service_layer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include

from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import obtain_jwt_token

from api_root.views import MovieSearchView, CreateUserView, \
    MovieRecommendationView


schema_view = get_schema_view(title='Moviexplorer API')

router = routers.DefaultRouter()
router.register(r'movies', MovieSearchView, base_name='movies')
router.register(r'recommendations', MovieRecommendationView, base_name='recommendations')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^register/$', CreateUserView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^api/schema/$', schema_view),
    url(r'^api/token/auth/', obtain_jwt_token),
]

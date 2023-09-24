"""HelloDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, include, re_path
from inverse.settings import MEDIA_ROOT, MEDIA_URL
from django.contrib import admin
from rest_framework import routers
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.views import *
from projects.views import *


schema_view = get_schema_view(
   openapi.Info(
      title='Inverse Projects API',
      default_version='v1',
      description='Платформа для проектной деятельности',
      terms_of_service='https://www.google.com/policies/terms/',
      contact=openapi.Contact(email='belogurov.ivan@list.ru'),
      license=openapi.License(name='BSD License'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Users
    path('api/users/students/', StudentAPIListView.as_view()),
    path('api/users/roles/', RoleAPIListView.as_view()),
    path('api/users/specialities/', SpecialityAPIListView.as_view()),
    path('api/users/skills/', SkillAPIListView.as_view()),
    path('api/users/classes/', ClassAPIListView.as_view()),
    path('api/users/auth/', include('djoser.urls')),
    re_path(r'^api/users/auth/', include('djoser.urls.authtoken')),

    #Projects
    path('api/projects/create/', ProjectAPICreateView.as_view()),
    path('api/projects/', ProjectAPIListView.as_view()),
    path('api/projects/my/', ProjectAPIMyListView.as_view()),
    path('api/projects/<int:pk>/', ProjectAPIDetailView.as_view()),
    path('api/projects/<int:pk>/vacancies/create/', VacancyAPICreateView.as_view()),
    path('api/projects/incoming-applications/create/', IncomingApplicationAPICreateView.as_view()),
    path('api/projects/incoming-applications/', IncomingApplicationAPIListView.as_view()),
    path('api/projects/incoming-applications/<int:pk>/accept/', IncomingApplicationAPIAcceptView.as_view()),
    path('api/projects/incoming-applications/<int:pk>/reject/', IncomingApplicationAPIRejectView.as_view()),
    path('api/projects/outgoing-applications/create/', OutgoingApplicationAPICreateView.as_view()),
    path('api/projects/outgoing-applications/', OutgoingApplicationAPIListView.as_view()),
    path('api/projects/outgoing-applications/<int:pk>/accept/', OutgoingApplicationAPIAcceptView.as_view()),
    path('api/projects/outgoing-applications/<int:pk>/reject/', OutgoingApplicationAPIRejectView.as_view()),
    path('api/projects/branches/', BranchAPIListView.as_view()),

    # Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
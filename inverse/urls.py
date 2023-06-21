from django.contrib import admin
from django.urls import path, re_path, include
from projects.views import *
from users.views import *
from teams.views import *


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Projects
    path('api/projects/', ProjectAPIListCreateView.as_view()),
    path('api/projects/my/', ProjectAPIMyListView.as_view()),
    path('api/projects/<int:pk>/', ProjectAPIDetailView.as_view()),
    path('api/projects/invites/my/', ProjectAPIMyInvitesView.as_view()),
    path('api/projects/<int:pk>/invites/send/', ProjectAPISendInviteView.as_view()),
    path('api/projects/<int:pk>/invites/confirm/', ProjectAPIConfirmInviteView.as_view()),
    path('api/projects/<int:pk>/invites/reject/', ProjectAPIRejectInviteView.as_view()),

    # Teams
    path('api/teams/', TeamAPIListCreateView.as_view()),
    path('api/teams/my/', TeamAPIMyListView.as_view()),
    path('api/teams/<int:pk>/', TeamAPIDetailView.as_view()),
    path('api/teams/invites/my/', TeamAPIMyInvitesView.as_view()),
    path('api/teams/<int:pk>/invites/send/', TeamAPISendInviteView.as_view()),
    path('api/teams/<int:pk>/invites/confirm/', TeamAPIRejectInviteView.as_view()),
    path('api/teams/<int:pk>/invites/reject/', TeamAPIConfirmInviteView.as_view()),

    # Users
    path('api/users/skills/', SkillAPIListCreateView.as_view()),
    path('api/users/students/', CustomUserAPIStudentsListView.as_view()),
    path('api/users/teachers/', CustomUserAPITeachersListView.as_view()),
    path('api/users/auth/', include('djoser.urls')),
    re_path(r'^api/users/auth/', include('djoser.urls.authtoken'))
]


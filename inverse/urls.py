from django.contrib import admin
from django.urls import path, re_path, include
from projects.views import ProjectAPIDetailView, ProjectAPIListCreateView, ProjectAPIMyListView, \
    ProjectAPISendInviteView, ProjectAPIConfirmInviteView, ProjectAPIRejectInviteView, ProjectAPIMyInvitesView
from users.views import SkillAPIListCreateView, CustomUserAPIStudentsListView, CustomUserAPITeachersListView

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

    # Users
    path('api/users/skills/', SkillAPIListCreateView.as_view()),
    path('api/users/students/', CustomUserAPIStudentsListView.as_view()),
    path('api/users/teachers/', CustomUserAPITeachersListView.as_view()),
    path('api/users/auth/', include('djoser.urls')),
    re_path(r'^api/users/auth/', include('djoser.urls.authtoken'))
]

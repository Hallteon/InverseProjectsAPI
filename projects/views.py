from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from projects.models import Project
from projects.permissions import IsProjectOwner, IsProjectOwnerOrInviter
from projects.serializers import ProjectSerializer
from django_currentuser.middleware import get_current_authenticated_user
from django.contrib.auth import get_user, get_user_model

from users.models import CustomUser


class ProjectAPIListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.filter(open=True)
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


class ProjectAPIMyListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(members__id=self.request.user.id)


class ProjectAPIRetrieveView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


class ProjectAPIUpdateView(generics.UpdateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwnerOrInviter]


class ProjectAPIDestroyView(generics.DestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwner]


class ProjectAPISendInviteView(generics.UpdateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwner]

    def update(self, request, *args, **kwargs):
        obj = Project.objects.get(pk=self.kwargs['project_pk'])
        invite_user = CustomUser.objects.get(pk=self.kwargs['user_pk'])

        obj.invites.add(invite_user.pk)
        obj.save()

        serializer = ProjectSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
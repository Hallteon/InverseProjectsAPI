from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from projects.models import Project
from projects.permissions import IsProjectOwner, IsProjectInviter, IsProjectClosedMember
from projects.serializers import ProjectSerializer
from users.models import CustomUser


class ProjectAPIListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(open=True, organization=self.request.user.organization.pk)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            project = Project.objects.get(pk=serializer.data['id'])

            project.organization = self.request.user.organization
            project.members.add(self.request.user.id)
            project.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectAPIMyListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(members__id=self.request.user.id)


class ProjectAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectClosedMember]

    def get_queryset(self):
        return Project.objects.filter(organization=self.request.user.organization.pk)


class ProjectAPIMyInvitesView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(invites__id=self.request.user.id)


class ProjectAPISendInviteView(generics.UpdateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectOwner]

    def update(self, request, *args, **kwargs):
        obj = Project.objects.get(pk=self.kwargs['pk'])
        user_uuid = request.GET.get('uuid', None)

        if user_uuid:
            invite_user = CustomUser.objects.get(user_uuid=user_uuid)

            if invite_user.organization.pk == obj.organization.pk:
                obj.invites.add(invite_user.pk)
                obj.save()

                serializer = ProjectSerializer(obj, required=False)

                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response("Something went wrong!", status=status.HTTP_400_BAD_REQUEST)


class ProjectAPIConfirmInviteView(generics.UpdateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectInviter]

    def update(self, request, *args, **kwargs):
        obj = Project.objects.get(pk=self.kwargs['pk'])
        invite_user = self.request.user

        if invite_user.role == 1:
            obj.members.add(invite_user.pk)

        elif invite_user.role == 2:
            obj.mentor = invite_user

        obj.invites.remove(invite_user.pk)
        obj.save()

        serializer = ProjectSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)


class ProjectAPIRejectInviteView(generics.UpdateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectInviter]

    def update(self, request, *args, **kwargs):
        obj = Project.objects.get(pk=self.kwargs['pk'])
        invite_user = self.request.user

        obj.invites.remove(invite_user.pk)
        obj.save()

        serializer = ProjectSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from teams.models import Team
from teams.permissions import *
from teams.serializers import TeamSerializer
from users.models import CustomUser


class TeamAPIListCreateView(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(open=True, organization=self.request.user.organization.pk)

    def post(self, request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            project = Team.objects.get(pk=serializer.data['id'])

            project.organization = self.request.user.organization
            project.members.add(self.request.user.id)
            project.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeamAPIMyListView(generics.ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(members__id=self.request.user.id)


class TeamAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsTeamClosedMember]

    def get_queryset(self):
        return Team.objects.filter(organization=self.request.user.organization.pk)


class TeamAPIMyInvitesView(generics.ListAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(invites__id=self.request.user.id)


class TeamAPISendInviteView(generics.UpdateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsTeamOwner]

    def update(self, request, *args, **kwargs):
        obj = Team.objects.get(pk=self.kwargs['pk'])
        user_uuid = request.GET.get('uuid', None)

        if user_uuid:
            invite_user = CustomUser.objects.get(user_uuid=user_uuid)

            if invite_user.organization.pk == obj.organization.pk:
                obj.invites.add(invite_user.pk)
                obj.save()

                serializer = TeamSerializer(obj, required=False)

                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response("Something went wrong!", status=status.HTTP_400_BAD_REQUEST)


class TeamAPIConfirmInviteView(generics.UpdateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsTeamInviter]

    def update(self, request, *args, **kwargs):
        obj = Team.objects.get(pk=self.kwargs['pk'])
        invite_user = self.request.user

        if invite_user.role == 1:
            obj.members.add(invite_user.pk)

        elif invite_user.role == 2:
            obj.mentor = invite_user

        obj.invites.remove(invite_user.pk)
        obj.save()

        serializer = TeamSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)


class TeamAPIRejectInviteView(generics.UpdateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsTeamInviter]

    def update(self, request, *args, **kwargs):
        obj = Team.objects.get(pk=self.kwargs['pk'])
        invite_user = self.request.user

        obj.invites.remove(invite_user.pk)
        obj.save()

        serializer = TeamSerializer(obj, required=False)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)




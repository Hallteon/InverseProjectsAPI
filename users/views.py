from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.serializers import SkillSerializer, CustomUserSerializer
from users.models import Skill, CustomUser


class SkillAPIListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.filter(skill_type=1)
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]


class CustomUserAPIStudentsListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(role=1, open=True, organization=self.request.user.organization.pk)


class CustomUserAPITeachersListView(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(role=2, open=True, organization=self.request.user.organization.pk)


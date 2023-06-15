from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.serializers import SkillSerializer, CustomUserSerializer
from users.models import Skill, CustomUser


class SkillAPIListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.filter(skill_type=1)
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]


class CustomUserAPIStudentsListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role__pk=1, open=True)
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class CustomUserAPITeachersListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role__pk=2)
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.serializers import SkillSerializer
from users.models import Skill


class SkillAPIListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.filter(skill_type=1)
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]



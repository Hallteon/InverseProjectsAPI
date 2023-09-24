from django.shortcuts import render
from rest_framework.permissions import *
from rest_framework import generics
from users.serializers import *
from users.models import *


class SpecialityAPIListView(generics.ListAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class SkillAPIListView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ClassAPIListView(generics.ListAPIView):
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.organization.classes.all()
    

class RoleAPIListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class StudentAPIListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(organization=self.request.user.organization, role__role_type='student', public=True)
    

    


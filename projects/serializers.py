from rest_framework import serializers
from projects.models import Project
from users.serializers import CustomUserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    members = CustomUserSerializer(many=True, required=False)
    mentor = CustomUserSerializer(required=False)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'teamlead', 'members', 'mentor', 'invites', 'open')

from rest_framework import serializers
from users.serializers import CustomUserSerializer, SkillSerializer, SpecialitySerializer
from projects.models import *


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name')


class VacancyReadSerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer(required=False)
    skills = SkillSerializer(many=True, required=False)

    class Meta:
        model = Vacancy
        fields = ('id', 'speciality', 'skills', 'description', 'open')


class VacancyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ('id', 'speciality', 'skills', 'description', 'open')


class MemberSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=False)
    vacancy = VacancyReadSerializer(required=False)

    class Meta:
        model = Member
        fields = ('id', 'user', 'vacancy')


class IncomingApplicationReadSerializer(serializers.ModelSerializer):
    user_from = CustomUserSerializer(required=False)
    vacancy = VacancyReadSerializer(required=False)

    class Meta:
        model = IncomingApplication
        fields = ('id', 'user_from', 'project', 'vacancy', 'annotation')


class IncomingApplicationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomingApplication
        fields = ('id', 'user_from', 'project', 'vacancy', 'annotation')


class OutgoingApplicationReadSerializer(serializers.ModelSerializer):
    user_to = CustomUserSerializer(required=False)
    vacancy = VacancyReadSerializer(required=False)

    class Meta:
        model = OutgoingApplication
        fields = ('id', 'user_to', 'project', 'vacancy')


class OutgoingApplicationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutgoingApplication
        fields = ('id', 'user_to', 'project', 'vacancy')


class ProjectReadDetailSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    branch = BranchSerializer(required=False)
    teamlead = CustomUserSerializer(required=False)
    members = MemberSerializer(many=True, required=False)
    vacancies = VacancyReadSerializer(many=True, required=False)
    incoming_applications = IncomingApplicationReadSerializer(many=True, required=False)
    outgoing_applications = OutgoingApplicationReadSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ('id', 'name', 'cover', 'description', 'branch', 'teamlead', 'members', 'vacancies', 'approved', 'incoming_applications', 'outgoing_applications')


class ProjectReadListSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    branch = BranchSerializer(required=False)

    class Meta:
        model = Project
        fields = ('id', 'name', 'cover', 'description', 'branch', 'teamlead', 'members', 'vacancies', 'approved', 'incoming_applications', 'outgoing_applications')


class ProjectWriteSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)

    class Meta:
        model = Project
        fields = ('id', 'name', 'cover', 'description', 'branch', 'teamlead', 'members', 'vacancies', 'approved', 'incoming_applications', 'outgoing_applications')


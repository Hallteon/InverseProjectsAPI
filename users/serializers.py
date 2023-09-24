from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import *


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'number', 'litera', 'faculty')


class OrganizationSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, required=False)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'description', 'address', 'classes')


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ('id', 'name')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'role_type')


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    cover = serializers.ImageField(required=False)

    class Meta(BaseUserRegistrationSerializer.Meta):
        model = get_user_model()
        fields = ('username', 'cover', 'firstname', 'lastname', 'bio', 'speciality', 'skills', 'email', 'telegram', 'phone_number', 'role', 'school_class', 'organization', 'public', 'password')


class CustomUserSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    role = RoleSerializer(required=False)
    speciality = SpecialitySerializer(required=False)
    skills = SkillSerializer(many=True, required=False)
    school_class = ClassSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'cover', 'firstname', 'lastname', 'bio', 'speciality', 'skills', 'email', 'telegram', 'phone_number', 'role', 'school_class', 'organization', 'public')


class CustomUserCurrentSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    role = RoleSerializer(required=False)
    speciality = SpecialitySerializer(required=False)
    skills = SkillSerializer(many=True, required=False)
    school_class = ClassSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'cover', 'firstname', 'lastname', 'bio', 'speciality', 'skills', 'email', 'telegram', 'phone_number', 'role', 'school_class', 'organization', 'public')
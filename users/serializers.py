from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Skill, Achievement


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'skill_type')


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'title', 'achievement_type')


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = get_user_model()
        fields = ('username', 'password')


class CustomUserSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(required=False, many=True)
    achievements = AchievementSerializer(required=False, many=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'firstname', 'lastname', 'bio', 'birthday', 'role', 'skills', 'experience',
                  'open', 'contacts', 'achievements', 'organization')


class CustomUserCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'firstname', 'lastname', 'bio', 'birthday', 'role', 'skills', 'experience',
                  'open', 'contacts', 'achievements', 'organization', 'user_uuid')

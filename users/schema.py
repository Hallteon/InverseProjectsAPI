import graphene
from graphene_django import DjangoObjectType
from users.models import CustomUser, Role, Skill, Achievement, Invite, Organization


# class SkillType(DjangoObjectType):
#     class Meta:
#


# class CustomUserType(DjangoObjectType):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'firstname', 'lastname', 'bio', 'birthday', 'role', 'experience', 'open', 'contacts',
#                   'organization', 'password')


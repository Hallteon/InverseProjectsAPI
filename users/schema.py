import graphene
from graphene_django import DjangoObjectType
from users.models import CustomUser, Role, Skill, Achievement, Invite, Organization
from django_currentuser.middleware import get_current_user


class SkillType(DjangoObjectType):
    class Meta:
        model = Skill
        fields = '__all__'


class RoleType(DjangoObjectType):
    class Meta:
        model = Role
        fields = '__all__'


class AchievementType(DjangoObjectType):
    class Meta:
        model = Achievement
        fields = '__all__'


class InviteType(DjangoObjectType):
    class Meta:
        model = Invite
        fields = '__all__'


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = '__all__'


class Query(graphene.ObjectType):
    organizations = graphene.List(OrganizationType)

    def resolve_organizations(self, info, **kwargs):
        return Organization.objects.all()


schema = graphene.Schema(query=Query)


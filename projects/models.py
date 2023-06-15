from django.db import models
from users.models import CustomUser, Organization
from django_currentuser.db.models import CurrentUserField


class Project(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    members = models.ManyToManyField(CustomUser, blank=True, related_name='projects_member', verbose_name='Участники')
    teamlead = CurrentUserField(on_delete=models.DO_NOTHING, verbose_name='Тимлид')
    mentor = models.ForeignKey(CustomUser, blank=True, null=True, related_name='projects_mentor', on_delete=models.DO_NOTHING, verbose_name='Наставник')
    invites = models.ManyToManyField(CustomUser, blank=True, related_name='projects_invites', verbose_name='Приглашения')
    open = models.BooleanField(default=True, verbose_name='Открытый проект')
    organization = models.ForeignKey(Organization, blank=True, null=True, related_name='projects_organization', on_delete=models.DO_NOTHING, verbose_name='Организация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
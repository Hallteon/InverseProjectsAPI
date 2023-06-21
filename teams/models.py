from django.db import models
from django_currentuser.db.models import CurrentUserField
from users.models import CustomUser, Organization


class Team(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    members = models.ManyToManyField(CustomUser, related_name='teams_member', verbose_name='Участники')
    teamlead = CurrentUserField(on_delete=models.DO_NOTHING, verbose_name='Тимлид')
    mentor = models.ForeignKey(CustomUser, related_name='teams_mentor', on_delete=models.DO_NOTHING, verbose_name='Ментор')
    invites = models.ManyToManyField(CustomUser, related_name='teams_invites', verbose_name='Приглашения')
    open = models.BooleanField(default=False, verbose_name='Открытая команда')
    organization = models.ForeignKey(Organization, related_name='teams_organization', on_delete=models.DO_NOTHING, verbose_name='Организация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

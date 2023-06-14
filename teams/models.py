from django.db import models
from users.models import CustomUser


class Team(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    members = models.ManyToManyField(CustomUser, related_name='teams_member', verbose_name='Участники')
    teamlead = models.ForeignKey(CustomUser, related_name='teams_teamlead', on_delete=models.DO_NOTHING, verbose_name='Тимлид')
    mentor = models.ForeignKey(CustomUser, related_name='teams_mentor', on_delete=models.DO_NOTHING, verbose_name='Ментор')
    invites = models.ManyToManyField(CustomUser, related_name='teams_invites', verbose_name='Приглашения')
    open = models.BooleanField(default=False, verbose_name='Открытая команда')

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

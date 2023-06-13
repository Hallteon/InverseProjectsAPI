from django.db import models
from users.models import CustomUser


class Group(models.Model):
    members = models.ManyToManyField(CustomUser, verbose_name='Участники')
    teamlead = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name='Тимлид')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Project(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    mentor = models.ForeignKey(CustomUser, verbose_name='Наставник')
    open = models.BooleanField(default=True, verbose_name='Открытый проект')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
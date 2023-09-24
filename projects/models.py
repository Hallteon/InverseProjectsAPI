import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django_currentuser.db.models import CurrentUserField
from users.models import CustomUser, Skill, Speciality


class Branch(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сфера'
        verbose_name_plural = 'Сферы'


class Vacancy(models.Model):
    speciality = models.ForeignKey(Speciality, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='vacancies_speciality', verbose_name='Специальность')
    skills = models.ManyToManyField(Skill, blank=True, related_name='vacancies_skill', verbose_name='Навык')
    description = models.TextField(blank=True, verbose_name='Описание')
    open = models.BooleanField(default=True, verbose_name='Вакансия открыта')

    def __str__(self):
        return self.speciality.name

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class IncomingApplication(models.Model):
    user_from = CurrentUserField(verbose_name='Отправитель')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='incoming_applications_project', verbose_name='Проект')
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE, related_name='incoming_applications_vacancy', verbose_name='Вакансия')
    annotation = models.TextField(blank=True, verbose_name='Аннотация')

    def __str__(self):
        return self.user_from.username

    class Meta:
        verbose_name = 'Входящая заявка'
        verbose_name_plural ='Входящие заявки'


class OutgoingApplication(models.Model):
    user_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='outgoing_applications_user', verbose_name='Пользователь')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='outgoing_applications_project', verbose_name='Проект')
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE, related_name='outgoing_applications_vacancy', verbose_name='Вакансия')
    
    def __str__(self):
        return self.user_to.username

    class Meta:
        verbose_name = 'Исходящая заявка'
        verbose_name_plural ='Исходящие заявки'


class Member(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='members_user', verbose_name='Пользователь')
    vacancy = models.ForeignKey('Vacancy', on_delete=models.DO_NOTHING, related_name='members_vacancy', verbose_name='Вакансия')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Project(models.Model):
    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        image_uuid = uuid.uuid1().hex
        return f'projects/covers/{image_uuid}.{extension}'

    name = models.CharField(max_length=256, verbose_name='Название')
    cover = models.ImageField(blank=True, null=True, upload_to=get_path, verbose_name='Обложка')
    description = models.TextField(blank=True, verbose_name='Описание')
    branch = models.ForeignKey('Branch', on_delete=models.DO_NOTHING, related_name='projects_branch', verbose_name='Сфера')
    teamlead = CurrentUserField(verbose_name='Тимлид')
    members = models.ManyToManyField('Member', blank=True, related_name='projects_members', verbose_name='Участники')
    vacancies = models.ManyToManyField('Vacancy', blank=True, related_name='projects_vacancy', verbose_name='Вакансии')
    approved = models.BooleanField(default=False, verbose_name='Одобрен')
    incoming_applications = models.ManyToManyField('IncomingApplication', blank=True, related_name='projects_incoming_application', verbose_name='Входящие заявки')
    outgoing_applications = models.ManyToManyField('OutgoingApplication', blank=True, related_name='projects_outcoming_application', verbose_name='Исходящие заявки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'



@receiver(pre_delete, sender=Project)
def event_model_delete(sender, instance, **kwargs):
    if instance.cover:
        instance.cover.delete(False)

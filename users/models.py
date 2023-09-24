import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Speciality(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class Skill(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'


class Class(models.Model):
    number = models.IntegerField(verbose_name='Цифра', validators=[MinValueValidator(1), MaxValueValidator(11)])
    litera = models.CharField(max_length=2, verbose_name='Литера')
    faculty = models.CharField(max_length=256, verbose_name='Направление')

    def __str__(self):
        return f'{self.number}{self.litera}'

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'


class Organization(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    address = models.TextField(verbose_name='Адрес')
    classes = models.ManyToManyField('Class', blank=True, related_name='organizations_class', verbose_name='Классы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Role(models.Model):
    name = models.CharField(max_length=256, verbose_name='Роль')
    role_type = models.CharField(max_length=100, verbose_name='Тип роли')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        image_uuid = uuid.uuid1().hex
        return f'users/avatars/{image_uuid}.{extension}'

    username = models.CharField(unique=True, max_length=256, verbose_name='Логин')
    cover = models.ImageField(blank=True, null=True, upload_to=get_path, verbose_name='Аватарка')
    firstname = models.CharField(max_length=256, blank=True, verbose_name='Имя')
    lastname = models.CharField(max_length=256, blank=True, verbose_name='Фамилия')
    bio = models.TextField(blank=True, null=True, verbose_name='Био')
    speciality = models.ForeignKey('Speciality', blank=True, null=True, on_delete=models.DO_NOTHING, related_name='users_speciality', verbose_name='Специальность')
    skills = models.ManyToManyField('Skill', blank=True, related_name='users_skill', verbose_name='Навык')
    email = models.EmailField(blank=True, null=True, verbose_name='Почта')
    telegram = models.CharField(max_length=256, blank=True, null=True, verbose_name='Telegram')
    phone_number = models.CharField(max_length=64, blank=True, null=True, verbose_name='Номер телефона')
    school_class = models.ForeignKey('Class', blank=True, null=True, on_delete=models.DO_NOTHING, related_name='users_class', verbose_name='Класс')
    organization = models.ForeignKey('Organization', blank=True, null=True, on_delete=models.CASCADE, related_name='users_organization', verbose_name='Организация')
    role = models.ForeignKey('Role', blank=True, null=True, on_delete=models.CASCADE, related_name='users_role', verbose_name='Роль')
    public = models.BooleanField(default=False, blank=True, verbose_name='Открытый аккаунт')
    password = models.CharField(max_length=256, verbose_name='Пароль')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'




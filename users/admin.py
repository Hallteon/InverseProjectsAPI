from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.forms import UserChangeForm, UserCreationForm
from users.models import *


class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'litera', 'faculty')
    search_fields = ('id', 'number', 'litera', 'faculty')
    list_filter = ('number', 'litera')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'address')
    search_fields = ('id', 'name', 'address')
    list_filter = ('name',)


class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('name',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role_type')
    search_fields = ('id', 'name', 'role_type')
    list_filter = ('name',)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'username', 'firstname', 'lastname', 'bio', 'speciality', 'email', 'telegram', 'phone_number', 'role', 'school_class', 'organization', 'public', 'is_superuser', 'cover')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'cover', 'firstname', 'lastname', 'bio', 'speciality', 'skills', 'email', 'telegram', 'phone_number', 'role', 'school_class', 'organization', 'public', 'password')}),
        ('Permissions', {'fields': ('is_superuser',)}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'cover', 'firstname', 'lastname', 'bio', 'speciality', 'skills', 'email', 'telegram', 'phone_number', 'role', 'school_class', 'organization', 'public', 'password1', 'password2'),
        }),)
    search_fields = ('username', 'email',)
    ordering = ('username', 'email',)
    filter_horizontal = ()


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
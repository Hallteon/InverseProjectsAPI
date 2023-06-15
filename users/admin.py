from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.apps import apps
from users.forms import UserChangeForm, UserCreationForm
from users.models import CustomUser, Skill, Achievement, Organization


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'skill_type')
    list_filter = ('id', 'skill_type')
    search_fields = ('id', 'name', 'skill_type')


class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'achieve_type')
    list_filter = ('title', 'achieve_type')
    search_fields = ('title',)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'address')
    list_filter = ('name', 'address')
    search_fields = ('name', 'address')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'user_uuid', 'username', 'email', 'firstname', 'lastname', 'bio', 'birthday', 'role', 'experience', 'open', 'contacts',
                    'organization', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'firstname', 'lastname', 'bio', 'birthday', 'role', 'experience', 'open',
                           'contacts', 'organization', 'password')}),
        ('Permissions', {'fields': ('is_superuser',)}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'firstname', 'lastname', 'bio', 'birthday', 'role', 'experience', 'open', 'contacts',
                       'organization', 'password1', 'password2'),
        }),)
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(Skill, SkillAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
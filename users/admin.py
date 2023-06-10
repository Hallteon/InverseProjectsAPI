from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.apps import apps
from users.forms import UserChangeForm, UserCreationForm
from users.models import CustomUser, Skill, Role, Invite, Achievement, Organization


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_filter = ('id', 'type')
    search_fields = ('id', 'name', 'type')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class InviteAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'message', 'accepted')
    list_filter = ('from_user', 'message', 'accepted')
    search_fields = ('from_user',)


class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'file')
    list_filter = ('title', 'type')
    search_fields = ('title',)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'address')
    list_filter = ('name', 'address')
    search_fields = ('name', 'address')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'firstname', 'lastname', 'bio', 'birthday', 'role', 'experience', 'open', 'contacts',
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
admin.site.register(Role, RoleAdmin)
admin.site.register(Invite, InviteAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)
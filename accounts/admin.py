from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'role']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'avatar', 'preferences')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('role', 'avatar', 'preferences')}),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'blends_created', 'blends_rated', 'get_subtaste_stats_preview']
    list_filter = ['blends_created', 'blends_rated']
    search_fields = ['user__username', 'user__email', 'subtaste_stats']
    
    def get_subtaste_stats_preview(self, obj):
        if obj.subtaste_stats:
            stats = list(obj.subtaste_stats.items())[:3]
            return ', '.join([f'{k}: {v}' for k, v in stats]) + ('...' if len(obj.subtaste_stats) > 3 else '')
        return 'Нет данных'
    get_subtaste_stats_preview.short_description = 'Статистика подвкусов (предпросмотр)'

@admin.register(UserBlendInteraction)
class UserBlendInteractionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'blend', 'rating', 'saved', 'created_by_user', 'published']
    list_filter = ['rating', 'saved', 'created_by_user', 'published']
    search_fields = [
        'user__username', 
        'user__email', 
        'blend__name',
        'blend__subtaste__name'
    ]

# Перерегистрируем MyUser с кастомным админом
admin.site.register(MyUser, CustomUserAdmin)
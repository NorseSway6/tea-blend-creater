from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class MyUser(AbstractUser):
    class Role(models.TextChoices):
        GUEST = 'guest', _('Гость')
        USER = 'user', _('Пользователь')
        ADMIN = 'admin', _('Администратор')
    
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    email = models.EmailField(max_length=255, unique=True, verbose_name=_('Email'))
    avatar = models.ImageField(upload_to='avatars/',blank=True, null=True)
    preferences = models.JSONField(default=list,blank=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN
    
    @property 
    def is_regular_user_role(self):
        return self.role == self.Role.USER
    
    @property
    def is_guest_role(self):
        return self.role == self.Role.GUEST

    def is_admin(self):
        return self.is_superuser or self.role == self.Role.ADMIN
    
    def is_regular_user(self):
        return self.role == self.Role.USER and not self.is_superuser
    
    def is_guest(self):
        return not self.is_authenticated or self.role == self.Role.GUEST
    
    def save(self, *args, **kwargs):
        if self.is_superuser or self.is_staff:
            self.role = self.Role.ADMIN
        elif not self.role:
            self.role = self.Role.USER
        if not self.preferences:
            self.preferences = {}
        
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='profile')
    blends_created = models.IntegerField()

    def __str__(self):
        return f'{self.user.username}'
    
    class Meta:
        db_table = 'user_profiles'


class UserBlendInteraction(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='blend_interactions')
    blend = models.ForeignKey('main_functionality.Blend', on_delete=models.CASCADE, related_name='user_interactions')
    rating = models.IntegerField(null=True, blank=True)
    saved = models.BooleanField(default=False)
    created_by_user = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user_blend_interactions'
        constraints = [
            models.UniqueConstraint(fields=['user', 'blend'], name='user_blend_fk')
        ]
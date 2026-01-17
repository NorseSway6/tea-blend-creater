from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class MyUser(AbstractUser):
    class Role(models.TextChoices):
        GUEST = 'guest'
        USER = 'user'
        ADMIN = 'admin'
    
    role = models.CharField(max_length=20,choices=Role.choices,default=Role.GUEST)
    email = models.EmailField(max_length=20)
    avatar = models.ImageField(upload_to='avatars/')
    preferences = models.JSONField(default=list,blank=True,)

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'
    
    class Meta:
        db_table = 'users'
    
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
    
    def is_regular_user(self):
        return self.role == self.Role.USER
    
    def is_guest(self):
        return self.role == self.Role.GUEST or not self.is_authenticated


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
    rating = models.IntegerField()
    saved = models.BooleanField()
    viewed = models.BooleanField(
        default=False,
        verbose_name=_('Просмотрено')
    )
    
    class Meta:
        db_table = 'user_blend_interactions'
        constraints = [
            models.UniqueConstraint(fields=['user', 'blend'], name='user_blend_fk')
        ]
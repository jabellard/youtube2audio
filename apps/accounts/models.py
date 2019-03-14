from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):
    pass


class User(AbstractUser):
    '''
    User model.
    '''

    user_id = models.AutoField(
        primary_key=True
    )
    email = models.EmailField(
        _('email address'),
        unique=True
    )

    def __str__(self):
        return '%s' % (self.username)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'user'

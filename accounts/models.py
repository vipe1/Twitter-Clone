from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

# Create your models here.
class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=24)
    # Usernmame field taken from Django source code with modified max_length
    username = models.CharField(
        _('username'),
        max_length=32,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    def __str__(self):
        if self.display_name != '':
            return self.display_name
        return self.username
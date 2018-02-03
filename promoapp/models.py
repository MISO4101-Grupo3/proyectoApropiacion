from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(UserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = email.lower();
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Meta:
        verbose_name_plural = "Usuarios"
    username = None
    email = models.EmailField(_('correo'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Categoria(models.Model):
    def __str__(self):
        return 'id:' + str(self.id)

    descripcion = models.CharField(null=False, blank=False, max_length=150, unique= True)


class Comentario(models.Model):
    def __str__(self):
        return 'id:' + str(self.id)

    texto = models.TextField(null=True, blank=True)
    correo = models.EmailField(null=True, blank=True)
    promocion = models.ForeignKey('Promocion', related_name='comentarios', null=False,
                                  on_delete=models.CASCADE)  # Promocion


class Promocion(models.Model):
    class Meta:
        verbose_name_plural = "promociones"
    def __str__(self):
        return 'id:' + str(self.id)

    nombre = models.CharField(null=False, blank=False, max_length=250)
    descripcion = models.TextField(null=True, blank=True)
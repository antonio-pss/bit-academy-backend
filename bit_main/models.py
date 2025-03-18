from django.core.validators import MinLengthValidator, MaxLengthValidator, validate_email
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class ModelBase(models.Model):
    id = models.BigAutoField(
        db_column='id',
        null=False,
        primary_key=True,
    )
    created_at = models.DateTimeField(
        db_column='dt_created_at',
        auto_now_add=True,
        verbose_name="Data de Criação",
        null=False,
    )
    modified_at = models.DateTimeField(
        db_column='dt_modified_at',
        auto_now=True,
        verbose_name="Última modificação",
        null=False,
    )
    active = models.BooleanField(
        db_column='cs_active',
        default=True,
        null=False,
    )

    class Meta:
        abstract = True
        managed = True


class User(ModelBase, AbstractUser):
    username = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=30,
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(20)
        ]
    )
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        unique=True,
        error_messages={"invalid": "O email fornecido não é válido!"}
    )
    xp = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        """Garante que a senha será armazenada corretamente como hash"""
        if self.password and (self._state.adding or not self.password.startswith("pbkdf2_sha256$")):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

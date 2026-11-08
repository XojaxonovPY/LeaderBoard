from django.apps import apps
from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db.models import ManyToManyField, ForeignKey, CASCADE, SET_NULL
from django.db.models import Model, CharField, TextChoices, DateTimeField, ImageField
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user_object(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, username, password, **extra_fields):
        user = self._create_user_object(username, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth.get_backends()
            if len(backends) == 1:
                backend = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractUser):
    class Meta:
        verbose_name = 'User'

    class RoleType(TextChoices):
        Admin = 'admin', 'Admin'
        Teacher = 'teacher', 'Teacher'
        Student = 'student', 'Student'

    username = CharField(
        max_length=150,
        unique=True,
        db_index=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages={"unique": _("A user with that username already exists."), },
    )
    first_name = None
    last_name = None
    email = None
    groups = None
    full_name = CharField(max_length=155, null=True, blank=True)
    password = CharField(max_length=155)
    role = CharField(max_length=30, choices=RoleType.choices)
    avatar = ImageField(upload_to='avatars/', null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class School(Model):
    name = CharField(max_length=75)

    def __str__(self):
        return self.name


class Group(Model):
    name = CharField(max_length=55)
    teacher = ForeignKey('users.User', on_delete=SET_NULL, related_name='teacher_groups', null=True, blank=True)
    school = ForeignKey('users.School', on_delete=CASCADE, related_name='groups')
    student = ManyToManyField('users.User', related_name='students_groups', blank=True)

    def __str__(self):
        return self.name


class Sessions(Model):
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='sessions')
    ip_address = CharField(max_length=200)
    device_name = CharField(max_length=200, db_index=True)
    last_login = DateTimeField(auto_now=True)
    expires_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device_name

from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, TextChoices, ForeignKey, CASCADE, DateTimeField, SET_NULL, ImageField


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user_object(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.role = "super admin"
        return user

    def _create_user(self, phone_number, password, **extra_fields):
        user = self._create_user_object(phone_number, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)

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

    first_name = None
    last_name = None
    username = None
    email = None
    full_name = CharField(max_length=155, null=True, blank=True)
    phone_number = CharField(max_length=20, unique=True)
    password = CharField(max_length=155)
    role = CharField(max_length=30, choices=RoleType, default=RoleType.Student)
    avatar = ImageField(upload_to='avatars/', null=True, blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    group = ForeignKey('users.Group', on_delete=SET_NULL, null=True, blank=True, related_name='users')
    objects = CustomUserManager()


class Course(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Group(Model):
    name = CharField(max_length=100)
    teacher = ForeignKey('users.User', on_delete=SET_NULL, related_name='teaching_groups', null=True, blank=True)
    course = ForeignKey('users.Course', on_delete=SET_NULL, related_name='course_groups', null=True, blank=True)

    def __str__(self):
        return self.name


class Sessions(Model):
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='sessions')
    ip_address = CharField(max_length=200)
    device_name = CharField(max_length=200)
    last_login = DateTimeField(auto_now=True)
    expires_at = DateTimeField(auto_now_add=True)

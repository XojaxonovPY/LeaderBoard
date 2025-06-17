from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import Model, CharField, TextChoices, ForeignKey, CASCADE, DateTimeField, SET_NULL, ImageField
from django.db.models.fields import PositiveIntegerField


class CustomUserManager(UserManager):

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("The given phone must be set")

        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    class Meta:
        verbose_name='users'
    class RoleType(TextChoices):
        Admin = 'admin', 'Admin'
        Teacher = 'teacher', 'Teacher'
        Student = 'student', 'Student'
    first_name = None
    last_name = None
    username = None
    email = None
    full_name = CharField(max_length=255)
    phone = CharField(max_length=20, unique=True)
    role = CharField(max_length=30, choices=RoleType, default=RoleType.Student)
    level = PositiveIntegerField(default=1)
    avatar = ImageField(upload_to='avatars/', null=True, blank=True)
    group = ForeignKey('auth_apps.Group', on_delete=SET_NULL, null=True, blank=True, related_name='users')
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Session(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='sessions')
    token = CharField(max_length=512)
    device_name = CharField(max_length=255)
    ip_address = CharField(max_length=50)
    last_login = DateTimeField()
    expires_at = DateTimeField()


class Course(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name

class Group(Model):
    name = CharField(max_length=100)
    teacher = ForeignKey('auth_apps.User', on_delete=SET_NULL, related_name='teaching_groups', null=True, blank=True)
    course = ForeignKey('auth_apps.Course', on_delete=SET_NULL, related_name='course_groups', null=True, blank=True)

    def __str__(self):
        return self.name

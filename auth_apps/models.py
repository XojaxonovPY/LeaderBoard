from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import Model, CharField, TextChoices, ForeignKey, CASCADE, BigIntegerField, SET_NULL, ImageField
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
    full_name=CharField(max_length=255)
    phone = CharField(max_length=20, unique=True)
    password = CharField(max_length=128, null=True, blank=True)
    role = CharField(max_length=30, choices=RoleType, default=RoleType.Student)
    level = PositiveIntegerField(default=1)
    avatar = ImageField(upload_to='avatars/', null=True, blank=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    course = ForeignKey('apps.Course', on_delete=SET_NULL,null=True,blank=True, related_name='users')
    objects = CustomUserManager()


class Badge(Model):
    name = CharField(max_length=255)
    icon = BigIntegerField()

    def __str__(self):
        return self.name


class UserBadge(Model):
    user = ForeignKey('auth_apps.User', on_delete=CASCADE, related_name='users')
    badge = ForeignKey('auth_apps.Badge', on_delete=CASCADE, related_name='badges')

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class Group(Model):
    name = CharField(max_length=100)
    course_id = BigIntegerField()
    users = ForeignKey('auth_apps.User', on_delete=SET_NULL, null=True,blank=True, related_name='group')

    def __str__(self):
        return self.name

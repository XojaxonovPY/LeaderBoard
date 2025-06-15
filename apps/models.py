from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey, CASCADE, TextField, JSONField, DateTimeField
from django.db.models import Model, URLField, BigIntegerField
from django.db.models import TextChoices, Model
from django.db.models.fields import CharField
from django.db.models.fields import PositiveIntegerField


class UploadedFile(models.Model):

    name = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else "Unnamed File"


class Course(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Submission(Model):
    class SubmissionType(TextChoices):
        FILE = "file", "File"
        LINK = "link", "Link"
        TEXT = "text", "Text"

    class StatusType(TextChoices):
        PENDING = "pending", "Pending"
        CHECKING = "checking", "Checking"
        GRADED = "graded", "Graded"
        REJECTED = "rejected", "Rejected"

    student_id = ForeignKey("auth_apps.User", on_delete=CASCADE, related_name='submissions')
    assignment_id = ForeignKey("apps.Assignment", on_delete=CASCADE, related_name='submissions')
    submission_type = CharField(max_length=255, choices=SubmissionType, default=SubmissionType.FILE)
    status = CharField(max_length=255, choices=StatusType, default=StatusType.PENDING)
    github_link = TextField()
    description = TextField()
    notes = TextField()
    score = TextField()
    feedback = TextField()
    detailed_review = JSONField(default=dict)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Assignment(Model):
    class DifficultyLevel(TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    class AssignmentType(TextChoices):
        HOMEWORK = "homework", "Homework"
        PROJECT = "project", "Project"
        QUIZ = "quiz", "Quiz"

    title = CharField(max_length=255)
    description = TextField()
    course = ForeignKey('apps.Course', on_delete=CASCADE, related_name='assignments')
    difficulty = CharField(max_length=20, choices=DifficultyLevel, default=DifficultyLevel.EASY)
    deadline = DateTimeField()
    assignment_type = CharField(max_length=20, choices=AssignmentType, default=AssignmentType.HOMEWORK)
    max_points=PositiveIntegerField(default=0)
    requirements = JSONField(default=list, blank=True)
    resources = JSONField(default=list, blank=True)

    def __str__(self):
        return self.title


class SubmissionFile(Model):
    url = URLField(max_length=200)
    submission = ForeignKey('apps.Submission', on_delete=CASCADE, related_name='files')
    name = CharField(max_length=255)
    size = BigIntegerField()

    def __str__(self):
        return self.name

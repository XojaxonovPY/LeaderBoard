from django.db.models import ForeignKey, CASCADE, TextField, DateTimeField, TextChoices, ManyToManyField, BooleanField
from django.db.models import Model, IntegerField, DateField, CharField, FileField, URLField, PositiveIntegerField


class Source(Model):
    name = CharField(max_length=125)
    link = URLField()
    created_at = DateTimeField(auto_now_add=True)
    lesson = ForeignKey("apps.Lesson", on_delete=CASCADE, related_name='sources')


class Lesson(Model):
    class StatusTextChoices(TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    name = CharField(max_length=155)
    description = TextField()
    presentation = FileField(upload_to="lessons/", null=True, blank=True)
    status = CharField(max_length=25, choices=StatusTextChoices.choices, default=StatusTextChoices.DRAFT)
    teacher = ForeignKey('users.User', on_delete=CASCADE, related_name='lessons')
    group = ManyToManyField('users.Group', related_name='lessons')
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Assignment(Model):
    title = CharField(max_length=255)
    description = TextField()
    score = IntegerField()
    lesson = ForeignKey("apps.Lesson", on_delete=CASCADE, related_name='assignments')
    start_date = DateField()
    deadline = DateTimeField()
    max_attempts = PositiveIntegerField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TestCase(Model):
    input_data = TextField(default="", blank=True)
    expected_output = TextField()
    is_hidden = BooleanField(default=False)
    points = PositiveIntegerField()
    assignment = ForeignKey('apps.Assignment', on_delete=CASCADE, related_name='tests')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'apps_test_cases'

    def __str__(self):
        test_type = "Hidden" if self.is_hidden else "Open"
        return f"{self.assignment.title} - #{self.id} ({test_type})"


class Submission(Model):
    class StatusTextChoices(TextChoices):
        SUBMITTED = "submitted", "Submitted"
        CHECKED = "checked", "Checked"
        REVISION = "revision", "Revision"

    assignment = ForeignKey('apps.Assignment', on_delete=CASCADE, related_name='submissions')
    student = ForeignKey('users.User', on_delete=CASCADE, related_name='submissions')
    submitted_at = DateTimeField(auto_now=True)
    ai_grade = IntegerField(default=0)
    final_grade = IntegerField(default=0)
    ai_feedback = TextField(null=True, blank=True)
    final_feedback = TextField(null=True, blank=True)
    status = CharField(max_length=25, choices=StatusTextChoices.choices, default=StatusTextChoices.SUBMITTED)
    attempt_count = PositiveIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.assignment.title


class SubmissionFile(Model):
    submission = ForeignKey('apps.Submission', on_delete=CASCADE, related_name='files')
    title = CharField(max_length=255)
    file_content = FileField(upload_to="submissions/", null=True, blank=True)
    text_content = TextField()
    is_copied = BooleanField(default=False)

    class Meta:
        db_table = 'apps_submission_files'

    def __str__(self):
        return self.title


class SubmissionResults(Model):
    submission = ForeignKey('apps.Submission', on_delete=CASCADE, related_name='results')
    test_case = ForeignKey('apps.TestCase', on_delete=CASCADE, related_name='results')
    is_passed = BooleanField(default=False)
    output = TextField(null=True, blank=True)
    error_message = TextField(null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('submission', 'test_case')
        db_table = 'apps_submission_results'

    def __str__(self):
        status = "Passed" if self.is_passed else "Failed"
        return f"Sub #{self.submission.id} - Test #{self.test_case.id}: {status}"

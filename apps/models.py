from django.db.models import ForeignKey, CASCADE, TextField, DateTimeField, SET_NULL, TextChoices
from django.db.models import Model, IntegerField, DateField,DecimalField,CharField,FileField


class Homework(Model):
    class FileType(TextChoices):
        PYTHON = ".py", "Python"
        JAVASCRIPT = ".js", "JavaScript"
        TYPESCRIPT = ".ts", "TypeScript"
        HTML = ".html", "HTML"
        CSS = ".css", "CSS"
        JSON = ".json", "JSON"
        YAML = ".yaml", "YAML"
        YML = ".yml", "YML"
        MARKDOWN = ".md", "Markdown"
        TXT = ".txt", "Text"
        JAVA = ".java", "Java"
        C = ".c", "C"
        CPP = ".cpp", "C++"
        CS = ".cs", "C#"
        GO = ".go", "Go"
        PHP = ".php", "PHP"
        RUBY = ".rb", "Ruby"
        RUST = ".rs", "Rust"

    title = CharField(max_length=255)
    description = TextField()
    points = IntegerField()
    start_date = DateField()
    deadline = DateTimeField()
    teacher = ForeignKey('auth_apps.User', on_delete=CASCADE, related_name='homeworks')
    group = ForeignKey('auth_apps.Group', on_delete=CASCADE, related_name='homeworks')
    file_extensions = CharField(max_length=255,choices=FileType,default=FileType.TXT)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Submission(Model):
    homework = ForeignKey('apps.Homework', on_delete=CASCADE, related_name='submissions')
    student = ForeignKey('auth_apps.User', on_delete=CASCADE, related_name='submissions')
    submitted_at = DateTimeField(auto_now=True)
    ai_grade = IntegerField(default=0)
    final_grade = IntegerField(default=0)
    ai_feedback = TextField(null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class SubmissionFile(Model):
    submission = ForeignKey('apps.Submission', on_delete=CASCADE, related_name='files')
    file_name = CharField(max_length=255)
    content = FileField()
    line_count = IntegerField()




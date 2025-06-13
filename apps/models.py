from django.db.models import Model, CharField, TextChoices

from django.db.models import ForeignKey, CASCADE, TextField, JSONField, DateTimeField

#
# class Submission(Model):
#     class SubmissionType(TextChoices):
#         File = "file,file"
#         Link = "link,link"
#         Text = "text,text"
#
#     class Status(TextChoices):
#         pending = "pending,pending",
#         checking = "checking,checking"
#         graded = "graded,graded"
#         rejected = "rejected,rejected"
#
#     student_id = ForeignKey("auth_apps.User", on_delete=CASCADE)
#     assignment_id = ForeignKey("auth_apps.Assignment", on_delete=CASCADE)
#     github_link = TextField()
#     description = TextField()
#     notes = TextField()
#     score = TextField()
#     feedback = TextField()
#     detailed_review = JSONField(default=dict)
#     created_at = DateTimeField(auto_now_add=True)
#     updated_at = DateTimeField(auto_now=True)
#
#
# class Course(Model):
#     name = CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Assignments(Model):
#     DIFFICULTY_CHOICES = [
#         ('easy', 'Easy'),
#         ('medium', 'Medium'),
#         ('hard', 'Hard'),
#     ]
#
#     ASSIGNMENT_TYPE_CHOICES = [
#         ('homework', 'Homework'),
#         ('project', 'Project'),
#         ('quiz', 'Quiz'),
#     ]
#
#     title = CharField(max_length=255)
#     description = TextField()
#     course = ForeignKey('Course', on_delete=CASCADE, related_name='assignments')
#     difficulty = CharField(max_length=10, choices=DIFFICULTY_CHOICES)
#     deadline = DateTimeField()
#     assignment_type = CharField(max_length=20, choices=ASSIGNMENT_TYPE_CHOICES)
#
#     def __str__(self):
#         return self.title


# nbksfjvbksf
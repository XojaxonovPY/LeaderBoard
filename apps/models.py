from django.db import models

class Submissions(models.Model):
    pass

class SubmissionFile(models.Model):
    url = models.URLField(max_length=200)
    submission = models.ForeignKey(Submissions, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    size = models.BigIntegerField()

    def __str__(self):
        return self.name







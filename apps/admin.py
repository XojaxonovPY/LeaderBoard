from django.contrib import admin
from django.contrib.admin import StackedInline

from apps.models import Homework, Submission, SubmissionFile


class SubmissionFileInline(StackedInline):
    model = SubmissionFile
    extra = 0
    readonly_fields = ('file_name', 'line_count')
    fields = ('file_name', 'content', 'line_count')


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    pass


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'submitted_at')
    inlines = [SubmissionFileInline]




# Admin interfeys uchun qo'shimcha sozlamalar
admin.site.site_header = "Homework Management System"
admin.site.site_title = "HMS Admin"
admin.site.index_title = "Boshqaruv Paneli"

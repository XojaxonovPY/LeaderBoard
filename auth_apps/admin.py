from django.contrib import admin

from auth_apps.models import User, Course, Group


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'full_name', 'group', 'role')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course')


# Django admin sozlamalari
admin.site.site_header = "🎓 Homework Management System"
admin.site.site_title = "HMS Admin"
admin.site.index_title = "🏠 Bosh sahifa - Boshqaruv paneli"

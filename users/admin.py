from django.contrib import admin

from users.models import User, School, Group


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'full_name', 'group', 'role')


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'school')


# Django admin sozlamalari
admin.site.site_header = "🎓 Homework Management System"
admin.site.site_title = "HMS Admin"
admin.site.index_title = "🏠 Bosh sahifa - Boshqaruv paneli"

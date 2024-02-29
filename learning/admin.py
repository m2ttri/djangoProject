from django.contrib import admin
from .models import Product, Access, Lesson, Group


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'start_datetime', 'cost', 'min_users', 'max_users']
    search_fields = ['author__username', 'title']
    raw_id_fields = ['author']


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'access_granted']


@admin.register(Lesson)
class LessonAdminAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'video_url']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'get_students_count']

    def get_students_count(self, obj):
        return obj.students.count()
    get_students_count.short_description = 'Students Count'

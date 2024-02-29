from rest_framework import serializers
from django.contrib.auth.models import User
from learning.models import Product, Lesson, Access, Group


class ProductSerializer(serializers.ModelSerializer):
    """
    Отображение списка все продуктов с отображением основной информации о продукте, количестве уроков которые
    принадлежат продукту, количестве учеников занимающихся на продукте, процент заполнения групп и
    процент приобретения продукта
    """

    start_datetime = serializers.DateTimeField(
        format='%d/%m/%Y %H:%M:',
        required=False,
        read_only=True
    )
    lessons_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    average_group_fill_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'start_datetime',
            'cost',
            'lessons_count',
            'students_count',
            'average_group_fill_percentage',
            'purchase_percentage'
        ]

    def get_lessons_count(self, obj):
        """Количестве уроков которые принадлежат продукту"""
        return obj.lessons.count()

    def get_students_count(self, obj):
        """Количестве учеников занимающихся на продукте"""
        return Access.objects.filter(product=obj, access_granted=True).count()

    def get_average_group_fill_percentage(self, obj):
        """Процент заполнения групп"""
        groups = Group.objects.filter(product=obj)
        if not groups:
            return 0
        total_percentage = sum(group.students.count() / obj.max_users * 100 for group in groups)
        return round(total_percentage / groups.count())

    def get_purchase_percentage(self, obj):
        """Процент приобретения продукта"""
        total_users = User.objects.count()
        product_accesses = Access.objects.filter(product=obj, access_granted=True).count()
        if total_users == 0:
            return 0
        return round((product_accesses / total_users) * 100)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'product']

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Count, Min
from learning.models import Access, Group


@receiver(post_save, sender=Access)
def distribute_user_to_group(sender, instance, created, **kwargs):
    """Распределение пользователей по группам при получении доступа к продукту"""

    if created and instance.access_granted:
        user = instance.user
        product = instance.product

        # Получаем все группы для данного продукта и подсчитываем количество студентов в каждой группе
        groups = Group.objects.filter(product=product).annotate(students_count=Count('students'))

        # Находим минимальное количество студентов среди всех групп
        min_students_count = groups.aggregate(Min('students_count'))['students_count__min']

        # Выбираем группы, в которых количество студентов равно минимальному и которые еще не достигли максимального
        # количества пользователей
        suitable_groups = groups.filter(students_count=min_students_count, students_count__lt=product.max_users)

        # Если продукт еще не начался и есть более одной подходящей группы, выбираем группу с наименьшим количеством
        # участников
        if product.start_datetime > timezone.now() and suitable_groups.count() > 1:
            group = suitable_groups.order_by('students_count').first()
        # В другом случае просто выбираем первую подходящую группу
        else:
            group = suitable_groups.first()

        # Если группа найдена, добавляем пользователя в эту группу
        if group:
            group.students.add(user)
        # Если группа не найдена, создаем новую группу и добавляем пользователя в нее
        else:
            new_group_title = f'Group for {product.title} #{Group.objects.filter(product=product).count() + 1}'
            new_group = Group.objects.create(product=product, title=new_group_title)
            new_group.students.add(user)



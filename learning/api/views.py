from rest_framework import generics
from learning.models import Product, Access, Lesson
from learning.api.serializers import ProductSerializer, LessonSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        user = self.request.user

        # Проверяем, авторизован ли пользователь
        if user.is_authenticated:
            # Проверяем, есть ли у пользователя доступ к продукту
            if Access.objects.filter(user=user, product__id=product_id, access_granted=True).exists():
                # Возвращаем уроки, связанные с продуктом
                return Lesson.objects.filter(product__id=product_id)
            else:
                # Если у пользователя нет доступа, возвращаем пустой queryset
                return Lesson.objects.none()
        else:
            # Если пользователь не авторизован, возвращаем пустой queryset
            return Lesson.objects.none()

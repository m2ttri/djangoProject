from django.urls import path
from . import views


app_name = 'learning'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/lessons/', views.LessonListView.as_view(), name='lesson-list'),

]

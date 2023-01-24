from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('reviews', views.ReviewViewSet)

app_name = 'main'
urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path('', include(router.urls)),
]

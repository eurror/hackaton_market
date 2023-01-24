from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework import filters

import django_filters

from .models import Category, Product, Order, OrderItem, Review, Like
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from .permission import IsAdminAuthPermission, IsAuthorPermission


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['tags__slug', 'created_at']
    ordering_fields = ['created_at', 'title']

    @action(['GET'], detail=True)
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        product = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(product=product, user=user)
            like.is_liked = not like.is_liked
            like.save()
            message = 'liked' if like.is_liked else 'disliked'
            if not like.is_liked:
                like.delete()
        except Like.DoesNotExist:
            Like.objects.create(product=product, user=user, is_liked=True)
            message = 'liked'
        return Response(message, status=200)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]

        return super().get_permissions()

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAdminAuthPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]

        return super().get_permissions()

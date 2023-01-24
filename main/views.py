from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
import django_filters
from rest_framework import filters

from .serializers import ProductSerializer, CategorySerializer
from .models import Category, Product, Order, OrderItem


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['tags__slug', 'created_at']
    ordering_fields = ['created_at', 'title']

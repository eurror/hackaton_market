from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)

    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise serializers.ValidationError('This category already exists')
        return title


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        product = Product.objects.create(user=user, **validated_data)
        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reviews'] = ReviewSerializer(
            Review.objects.filter(product=instance.pk), many=True).data
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.name')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Review.objects.create(user=user, **validated_data)
        return comment

    class Meta:
        model = Review
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'category', 'created_at']


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'title', 'price'

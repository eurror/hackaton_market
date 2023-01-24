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
    class Meta:
        model = Product
        fields = ('title', 'category', 'price', 'available', 'created', 'updated')

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Review.objects.create(author=user, **validated_data)
        return comment

    class Meta:
        model = Review
        fields = '__all__'



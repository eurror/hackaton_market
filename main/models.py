from django.db import models

from PIL import Image

from account.models import User


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['title', ]

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        instance = super(Product, self).save(*args, **kwargs)
        image = Image.open(instance.image.path)
        image.save(instance.image.path, quality=20, optimize=True)
        return instance

    class Meta:
        ordering = ['title', ]

    def __str__(self):
        return self.title


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = '-created',

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='likes')
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product} is liked by {self.user}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        return self.text

    class Meta:
        ordering = ['-created']

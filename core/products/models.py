from unicodedata import category
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    thumbnail = models.URLField(null=True, blank=True, max_length=1000)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    category = models.ForeignKey(
        Category, related_name='sub_categories', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.TextField()
    thumbnail = models.URLField(null=True, blank=True, max_length=1000)
    urls = models.URLField(null=True, blank=True, max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    productId = models.IntegerField()
    available = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    source = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

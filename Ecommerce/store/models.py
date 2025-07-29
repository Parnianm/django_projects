from django.db import models
from category.models import Category

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    

class VariationCategory(models.Model):
    name = models.CharField(max_length=50)  
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # ForeignKey to Product
    category = models.ForeignKey(VariationCategory, on_delete=models.CASCADE)  # ForeignKey to VariationCategory
    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)  # Added this field
    modified_date = models.DateTimeField(auto_now=True) 

    def __str__(self):
         return f"{self.product.product_name} - {self.category.name}: {self.value}"
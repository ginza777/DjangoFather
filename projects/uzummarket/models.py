from django.db import models

# Create your models here.

class Shop(models.Model):
    nomi= models.CharField(max_length=100)
    manzili = models.CharField(max_length=100)
    telefon = models.CharField(max_length=100)
    extra = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nomi


class  Vendor(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Product(models.Model):
    nomi= models.CharField(max_length=100)
    rasmi = models.ImageField(upload_to='./static/products')


    def __str__(self):
        return self.nomi


class Order(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.nomi




from django.db import models
from django.contrib.auth.models import User
from payments.models import Transaction

# Create your models here.
class Product (models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(default='default_prod.jpg', upload_to='product_images')

    def __str__(self):
        return self.title

class CartProduct (models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)



class Order (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartProduct, blank=True, default = [])
    placed = models.BooleanField(default = "False")
    order_time = models.DateTimeField(blank = True, null = True)
    amount = models.DecimalField(decimal_places=2, max_digits=15, default = 0)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, null=True, blank=True)

    




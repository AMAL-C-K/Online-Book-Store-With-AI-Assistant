from django.db import models
from django.contrib.auth.models import User

from products_app.models import Book


class Order(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.FloatField()
    payment_method = models.CharField(max_length=50, default='Cash on Delivery')
    status = models.CharField(max_length=50, default='Order Placed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book.title
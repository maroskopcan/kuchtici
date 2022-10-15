from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Receipt(models.Model):
    rec_title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    rating = models.DecimalField(decimal_places=0, max_digits=3)
    process = models.TextField(blank=True)

class Ingredients(models.Model):
    rec_id = models.ManyToManyField(
        Receipt, related_name="receipts",
    )
    quantity = models.DecimalField(decimal_places=2, max_digits=5)
    unit = models.CharField(max_length=16)
    ingr_name = models.CharField(max_length=64)
    price = models.DecimalField(decimal_places=2, max_digits=6, blank=True)

class Category(models.Model):
    category_id = models.ManyToManyField(
        Receipt, related_name="category",
    )
    category_name = models.CharField(max_length=64, blank=True)
class ReceiptRating(models.Model):
    receipt = models.ForeignKey(
        Receipt, related_name="review",
        on_delete=models.CASCADE
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        get_user_model(), related_name="user_reviews",
        on_delete=models.CASCADE
    )
    text = models.TextField()




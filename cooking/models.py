from django.db import models


class Receipts(models.Model):
    rec_title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    rating = models.DecimalField(decimal_places=0, max_digits=3)
    process = models.TextField(blank=True)

class Ingredients(models.Model):
    rec_id = models.ManyToManyField(
        Receipts, related_name="receipts",
    )
    quantity = models.DecimalField(decimal_places=2, max_digits=5)
    unit = models.CharField(max_length=16)
    ingr_name = models.CharField(max_length=64)
    price = models.DecimalField(decimal_places=2,max_digits=6, blank=True)






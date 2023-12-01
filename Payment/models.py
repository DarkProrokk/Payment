from django.db import models


# Create your models here.


class Item(models.Model):
    CUR = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(max_length=30, choices=CUR, default='usd')

    def __str__(self):
        return f'{self.name} --- ID {self.pk}'


class Discount(models.Model):
    percent_off = models.FloatField()
    discount_hash = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.percent_off}'


class Tax(models.Model):
    display_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    percentage = models.FloatField()
    inclusive = models.BooleanField()
    tax_hash = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.display_name} + {self.percentage} + {self.inclusive}'


class Order(models.Model):
    items = models.ManyToManyField(Item, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, blank=True, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.pk

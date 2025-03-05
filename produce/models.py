from django.db import models
from batches.models import BatchProduce
from django.db.models import Sum

class Produce(models.Model):
    name = models.CharField(max_length=255)  # Item Name
    demand = models.CharField(max_length=50, choices=[
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
    ])
    type = models.CharField(max_length=50, choices=[
        ("vegetable", "Vegetable"),
        ("fruit", "Fruit"),
        ("grain", "Grain"),
        ("dairy", "Dairy"),
        ("meat", "Meat"),
        ("other", "Other")
    ])
    check_frequency = models.CharField(max_length=20)  # "2 / week"
    image = models.ImageField(upload_to="produce_images/", null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

    def left_in_stock(self):
        return BatchProduce.objects.filter(produce=self).aggregate(sum=Sum('left_in_stock'))['sum']
    
    def is_low_on_supply(self):
        initial_stock = BatchProduce.objects.filter(produce=self).aggregate(sum=Sum('initial_stock'))['sum']
        average_demand = initial_stock / BatchProduce.objects.filter(produce=self).count()
        return self.left_in_stock() < average_demand / 5
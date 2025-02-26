from django.db import models

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

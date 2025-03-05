from django.db import models
# from produce.models import Produce

from django.apps import apps

class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    batch_manager = models.ForeignKey("accounts.ManagerUser", on_delete=models.CASCADE, related_name="manager_assigned_to_batch")
    added_to_inventory_on = models.DateField()

    def __str__(self):
        return f"Batch {self.batch_id}, managed by {self.manager_assigned}"


class BatchProduce(models.Model):
    batch = models.ForeignKey("batches.Batch", on_delete=models.CASCADE, related_name="batch_produce")
    produce = models.ForeignKey("produce.Produce", on_delete=models.CASCADE, related_name="batch_entries")
    health_on_arrival = models.CharField(max_length=50, choices=[
        ("very good", "Very Good"),
        ("good", "Good"),
        ("bad", "Bad"),
        ("unknown", "Unknown")
    ])
    expected_to_last_until = models.DateField()
    left_in_stock = models.PositiveIntegerField(default=0)
    initial_stock = models.PositiveIntegerField(default=0)
    is_spoiled = models.BooleanField(default=False)
    purchased_from = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["batch", "produce"], name="unique_batch_produce")
        ]

    def __str__(self):
        return f"{self.produce.name} in Batch {self.batch.id}"
    
    def used(initial_stock, left_in_stock):
        return initial_stock - left_in_stock
    
    def is_most_recent_batch_of_a_produce(self):
        latest_date = BatchProduce.objects.filter(produce=self.produce).aggregate(Max('batch__date_arrived'))['batch__date_arrived__max']
        return self.batch.added_to_inventory_on == latest_date
        

class HealthCheck(models.Model):
    batch_produce = models.ForeignKey(BatchProduce, on_delete=models.CASCADE, related_name="health_checks")
    health_status = models.CharField(max_length=50, choices=[
        ("very good", "Very Good"),
        ("good", "Good"),
        ("average", "Average"),
        ("bad", "Bad"),
        ("unknown", "Unknown")
    ])
    checked_on = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"Health Check - {self.batch_produce.produce.name} (Batch {self.batch_produce.batch.batch_id})"

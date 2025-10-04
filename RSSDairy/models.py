# from django.db import models

# class RfidScan(models.Model):
#     uid = models.CharField(max_length=50)            # e.g. "123456"
#     name = models.CharField(max_length=100)          # e.g. "desh"
#     block = models.CharField(max_length=10)          # e.g. "A"
#     time = models.TimeField()                        # e.g. 15:55
#     date = models.DateField()                        # e.g. 2025-10-03

#     def __str__(self):
#         return f"{self.name}  ({self.uid}) - {self.date} {self.time}"
from django.db import models

class RfidScan(models.Model):
    uid = models.CharField(max_length=50, unique=True)  # one row per tag
    name = models.CharField(max_length=100)
    block = models.CharField(max_length=10)
    time = models.TimeField()   # from device (or make server-side if you prefer)
    date = models.DateField()   # from device (or make server-side if you prefer)
    updated_at = models.DateTimeField(auto_now=True)  # useful for ordering/display

    def __str__(self):
        return f"{self.name} ({self.uid}) - {self.date} {self.time}"

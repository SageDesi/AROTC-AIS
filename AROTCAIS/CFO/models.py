from django.db import models

# Create your models here.

class SuperCOA(models.Model):
    SuperID = models.IntegerField(null=False, blank=False)

class COA(models.Model):
    SuperID = models.ForeignKey(SuperCOA, on_delete=models.CASCADE)
    SubID = models.AutoField(primary_key=True)
    composite_key = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        self.composite_key = f"{self.SuperID_id}_{self.sub_id}"
        super().save(*args, **kwargs)
        
    AccountName = models.CharField(max_length=30, null=True, blank=True)
    To_Increase = models.CharField(max_length=10, null=False, blank=False)
    AccountCategory = models.CharField(max_length=15, null=False, blank=False)
    AccountDesciption = models.CharField(max_length=100, null=True, blank=True)
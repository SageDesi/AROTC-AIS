from django.db import models
# Create your models here.

class SuperCOA(models.Model):
    SuperID = models.IntegerField(null=False, blank=False, primary_key=True)
    SuperID_Name = models.CharField(max_length=30, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return "ID: " + str(self.SuperID) + " Account Name: " + str(self.SuperID_Name)

class COA(models.Model):
    SuperID =  models.IntegerField(null=True, blank=True, primary_key=False)
    SubID = models.IntegerField(null=True, blank=True, primary_key=False)
    concatenated_id = models.CharField(max_length=100, unique=True, primary_key=True)

    class Meta:
        unique_together = ('SuperID','SubID')
    
    def save(self, *args, **kwargs):
        self.concatenated_id = str(self.SuperID) + str(self.SubID)
        super().save(*args, **kwargs)
        
    AccountName = models.CharField(max_length=30, null=True, blank=True)
    To_Increase = models.CharField(max_length=10, null=False, blank=False)
    AccountCategory = models.CharField(max_length=15, null=False, blank=False)
    AccountDescription = models.CharField(max_length=500, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return "ID: " + str(self.concatenated_id) + " Account Name: " + str(self.AccountName) + " Account Category: " + str(self.AccountCategory)
    
    def getPK(self):
        return self.pk


class JournalEntry(models.Model):
    JournalID = models.AutoField(primary_key=True)
    DateRealized = models.DateTimeField(auto_now=False, null=True)
    DateInputted = models.DateTimeField(auto_now=False, null=True)
    JournalDescription = models.CharField(max_length=500, null=True, blank=True)
    Receipt = models.ImageField(upload_to='images/', null=True)
    objects = models.Manager()

class DebitedAccount(models.Model):
    # JournalID = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)
    COA_ID = models.ForeignKey(COA, on_delete=models.CASCADE)
    DebitID = models.AutoField(primary_key=True)
    DebitAmount = models.DecimalField(max_digits=10, decimal_places=2)
    objects = models.Manager()

    def __str__(self):
        return "Account: " + str(self.COA_ID) + " | Debited Amount: " + str(self.DebitAmount)


class CreditedAccount(models.Model):
    # JournalID = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)
    COA_ID = models.ForeignKey(COA, on_delete=models.CASCADE)
    CreditID = models.AutoField(primary_key=True)
    CreditAmount = models.DecimalField(max_digits=10, decimal_places=2)
    objects = models.Manager()

    def __str__(self):
        return "Account: " + str(self.COA_ID) + " | Credited Amount: " + str(self.CreditAmount)
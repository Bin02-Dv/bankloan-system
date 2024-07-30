from django.db import models

# Create your models here.

class Loan(models.Model):
    name = models.CharField(max_length=225)
    loan_amount = models.CharField(max_length=225)
    loan_status = models.CharField(max_length=225)

    def __str__(self):
        return self.name
